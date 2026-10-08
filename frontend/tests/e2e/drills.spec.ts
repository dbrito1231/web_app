import { test, expect } from "@playwright/test";

// Phase 4 (plan p4_drill_list_ui): N4 drill labels, N9 question above the grid, Next drill.
test.describe("drill list UI", () => {
  test("N4: Start here lists drills with type and stem preview, ID muted", async ({ page }) => {
    await page.goto("/start?lesson=lesson-1-1");
    const link = page.locator("a[href^='/exam?q=q-saa-1-1-']").first();
    await expect(link).toBeVisible({ timeout: 15_000 });
    await expect(link).toHaveText(/^(MC|MR) · .{10,}/);
    await expect(link).not.toHaveText(/^q-saa/);
    await expect(page.locator(".drill-id").first()).toContainText("q-saa-1-1-");
  });

  test("N9: ?q= opens with the question above the grid and focus on its heading", async ({ page }) => {
    await page.goto("/exam?q=q-saa-1-1-k01-mc");
    const heading = page.locator("h2.pbq-heading");
    await expect(heading).toHaveText("q-saa-1-1-k01-mc", { timeout: 15_000 });
    await expect(heading).toBeFocused();
    const order = await page.evaluate(() => {
      const a = document.querySelector("article.pbq")!.getBoundingClientRect().top;
      const g = document.querySelector(".pbq-grid")!.getBoundingClientRect().top;
      return a < g;
    });
    expect(order).toBe(true);
  });

  test("N9: card click opens that drill without a long scroll, at 375 px", async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 812 });
    await page.goto("/exam?q=q-saa-1-1-k01-mc");
    await expect(page.locator("h2.pbq-heading")).toHaveText("q-saa-1-1-k01-mc", { timeout: 15_000 });
    await page.locator(".pbq-card", { hasText: /./ }).nth(3).click();
    await expect(page.locator("h2.pbq-heading")).not.toHaveText("q-saa-1-1-k01-mc");
    await expect(page.locator("h2.pbq-heading")).toBeFocused();
    const noHScroll = await page.evaluate(
      () => document.documentElement.scrollWidth <= document.documentElement.clientWidth,
    );
    expect(noHScroll).toBe(true);
  });

  test("Next drill opens the next drill in the list and focuses its heading", async ({ page }) => {
    await page.goto("/exam?q=q-saa-1-1-k01-mc");
    const heading = page.locator("h2.pbq-heading");
    await expect(heading).toHaveText("q-saa-1-1-k01-mc", { timeout: 15_000 });
    await page.getByRole("radio").first().check();
    await page.getByRole("button", { name: "Check answers" }).click();
    await page.getByRole("button", { name: "Next drill" }).click();
    await expect(heading).not.toHaveText("q-saa-1-1-k01-mc");
    await expect(heading).toBeFocused();
  });
});
