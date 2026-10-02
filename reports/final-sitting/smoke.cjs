// Browser smoke test against a throwaway local DB. Run from frontend/.
const { chromium } = require('/home/user/web_app/frontend/node_modules/playwright');
const fs = require('fs');
const Q = (id) => JSON.parse(fs.readFileSync(`/home/user/web_app/content/questions/${id}.json`, 'utf8'));
const APP = 'http://127.0.0.1:5173';

// ~10 questions across 3.1 to tf-g8, incl. ones edited this sitting
const right = ['q-saa-3-1-k01-mc', 'q-saa-3-3-k01-mr', 'q-saa-3-5-k07-mr', 'q-saa-3-5-s04-mc',
  'q-saa-4-2-k01-mc', 'q-saa-4-4-k05-mc', 'q-tf-004-1a-mr', 'q-tf-004-4a-mc',
  'q-tf-004-7b-mc2', 'q-tf-004-8b-mc'];
const wrong = 'q-tf-004-8c-mc2';

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const page = await browser.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  let pass = 0, fail = 0;
  const log = (ok, msg) => { ok ? pass++ : fail++; console.log(`${ok ? 'PASS' : 'FAIL'} ${msg}`); };

  async function answer(id, pickCorrect) {
    const q = Q(id);
    if (!fs.existsSync(`/home/user/web_app/content/questions/${id}.json`)) return log(false, `${id} missing`);
    await page.goto(`${APP}/exam?q=${encodeURIComponent(id)}`);
    await page.locator('h2.pbq-heading', { hasText: id }).waitFor({ timeout: 15000 });
    const ids = pickCorrect ? q.correctAnswerIds
      : q.choices.map((c) => c.id).filter((c) => !q.correctAnswerIds.includes(c)).slice(0, q.correctAnswerIds.length);
    for (const cid of ids) {
      const text = q.choices.find((c) => c.id === cid).text;
      await page.locator('label.choice-row', { hasText: text }).locator('input').check();
    }
    await page.getByRole('button', { name: 'Check answers' }).click();
    const verdict = await page.locator('.rationale strong').first().textContent({ timeout: 15000 });
    const want = pickCorrect ? 'Correct' : 'Incorrect';
    log(verdict === want, `${id}: expected ${want}, got ${verdict}`);
  }

  for (const id of right) { try { await answer(id, true); } catch (e) { log(false, `${id}: ${e.message.split('\n')[0]}`); } }
  try { await answer(wrong, false); } catch (e) { log(false, `${wrong}: ${e.message.split('\n')[0]}`); }

  // Lessons edited this sitting show the new text
  const lessonChecks = [
    ['lesson-3-5', 'one of two engines', 'Glue for Ray'],
    ['lesson-4-4', 'ECMP enabled', null],
    ['lesson-3-3', 'ReplicaLag', null],
  ];
  for (const [lid, must, mustNot] of lessonChecks) {
    try {
      const r = await page.request.get(`http://127.0.0.1:8000/api/lessons/${lid}`);
      const body = await r.text();
      log(r.ok() && body.includes(must) && (!mustNot || !body.includes(mustNot)),
        `${lid} API serves new text "${must}"${mustNot ? ` and no "${mustNot}"` : ''}`);
    } catch (e) { log(false, `${lid}: ${e.message}`); }
  }
  // Start here renders a lesson body in the browser
  try {
    await page.goto(`${APP}/start?lesson=lesson-tf-g8`);
    await page.getByText('HCP Terraform', { exact: false }).first().waitFor({ timeout: 15000 });
    log(true, 'Start here renders lesson-tf-g8');
  } catch (e) { log(false, `Start here lesson-tf-g8: ${e.message.split('\n')[0]}`); }

  // Progress recorded the attempts in the throwaway DB
  const prog = await (await page.request.get('http://127.0.0.1:8000/api/progress')).json().catch(() => null);
  console.log('progress:', JSON.stringify(prog).slice(0, 300));
  log(errors.length === 0, `no page errors (${errors.length})`);
  console.log(`\nRESULT: ${pass} pass, ${fail} fail`);
  await browser.close();
  process.exit(fail ? 1 : 0);
})();
