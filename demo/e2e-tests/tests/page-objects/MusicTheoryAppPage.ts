import { Page, Locator, expect } from '@playwright/test';

export class MusicTheoryAppPage {
  readonly page: Page;

  // Input elements
  readonly chordProgressionInput: Locator;
  readonly analyzeButton: Locator;
  readonly clearButton: Locator;
  readonly inputMethodDropdown: Locator;

  // Navigation
  readonly analysisHubTab: Locator;
  readonly scaleFinderTab: Locator;

  // Analysis results
  readonly resultsPanel: Locator;
  readonly functionalAnalysis: Locator;
  readonly modalAnalysis: Locator;
  readonly chromaticAnalysis: Locator;
  readonly confidenceScore: Locator;
  readonly romanNumerals: Locator;
  readonly keyCenter: Locator;
  readonly modeDisplay: Locator;

  // UI state indicators
  readonly loadingSpinner: Locator;
  readonly errorMessage: Locator;
  readonly successIndicator: Locator;

  constructor(page: Page) {
    this.page = page;

    // Input elements
    this.chordProgressionInput = page.locator('[data-testid="chord-progression-input"]');
    this.analyzeButton = page.locator('[data-testid="analyze-button"]');
    this.clearButton = page.locator('[data-testid="clear-button"]');
    this.inputMethodDropdown = page.locator('[data-testid="input-method-dropdown"]');

    // Navigation
    this.analysisHubTab = page.locator('[data-testid="analysis-hub-tab"]');
    this.scaleFinderTab = page.locator('[data-testid="scale-finder-tab"]');

    // Analysis results
    this.resultsPanel = page.locator('[data-testid="results-panel"]');
    this.functionalAnalysis = page.locator('[data-testid="functional-analysis"]');
    this.modalAnalysis = page.locator('[data-testid="modal-analysis"]');
    this.chromaticAnalysis = page.locator('[data-testid="chromatic-analysis"]');
    this.confidenceScore = page.locator('[data-testid="confidence-score"]');
    this.romanNumerals = page.locator('[data-testid="roman-numerals"]');
    this.keyCenter = page.locator('[data-testid="key-center"]');
    this.modeDisplay = page.locator('[data-testid="mode-display"]');

    // UI state indicators
    this.loadingSpinner = page.locator('[data-testid="loading-spinner"]');
    this.errorMessage = page.locator('[data-testid="error-message"]');
    this.successIndicator = page.locator('[data-testid="success-indicator"]');
  }

  async navigateToApp() {
    await this.page.goto('/');
    await this.page.waitForLoadState('networkidle');
  }

  async navigateToAnalysisHub() {
    await this.navigateToApp();
    if (await this.analysisHubTab.isVisible()) {
      await this.analysisHubTab.click();
    }
    await this.waitForPageReady();
  }

  async navigateToScaleFinder() {
    await this.navigateToApp();
    if (await this.scaleFinderTab.isVisible()) {
      await this.scaleFinderTab.click();
    }
    await this.waitForPageReady();
  }

  async waitForPageReady() {
    await this.page.waitForLoadState('networkidle');
    // Wait for any loading spinners to disappear
    await this.page.waitForFunction(() => {
      const spinners = document.querySelectorAll('[data-testid="loading-spinner"]');
      return Array.from(spinners).every(spinner => spinner.style.display === 'none' || !spinner.isConnected);
    }, { timeout: 10000 });
  }

  async enterInput(input: string, inputType: 'chord-progression' | 'scale' | 'melody' | 'single-chord' = 'chord-progression') {
    // Select appropriate input method if dropdown exists
    if (await this.inputMethodDropdown.isVisible()) {
      await this.inputMethodDropdown.click();

      const methodOption = inputType === 'chord-progression' ? 'Chord Progression' :
                          inputType === 'scale' ? 'Scale/Notes' :
                          inputType === 'melody' ? 'Melody' : 'Chord Progression';

      await this.page.locator(`text="${methodOption}"`).click();
    }

    // Clear existing input
    await this.chordProgressionInput.clear();

    // Enter the input
    await this.chordProgressionInput.fill(input);

    // Wait a moment for any auto-detection
    await this.page.waitForTimeout(500);
  }

  async clickAnalyze() {
    await this.analyzeButton.click();
  }

  async analyzeInput(input: string, inputType: 'chord-progression' | 'scale' | 'melody' | 'single-chord' = 'chord-progression') {
    await this.enterInput(input, inputType);
    await this.clickAnalyze();
    await this.waitForAnalysisComplete();
  }

  async waitForAnalysisComplete(timeout = 10000) {
    // Wait for loading to start (optional)
    try {
      await this.loadingSpinner.waitFor({ state: 'visible', timeout: 1000 });
    } catch {
      // Loading might be too fast to catch
    }

    // Wait for loading to complete
    await this.loadingSpinner.waitFor({ state: 'hidden', timeout });

    // Wait for results to appear
    await this.resultsPanel.waitFor({ state: 'visible', timeout });

    // Give a moment for all animations/updates to complete
    await this.page.waitForTimeout(500);
  }

  async expectAnalysisType(type: 'functional' | 'modal' | 'chromatic' | 'chord' | 'scale' | 'melodic') {
    const analysisMap = {
      functional: this.functionalAnalysis,
      modal: this.modalAnalysis,
      chromatic: this.chromaticAnalysis,
      chord: this.page.locator('[data-testid="chord-analysis"]'),
      scale: this.page.locator('[data-testid="scale-analysis"]'),
      melodic: this.page.locator('[data-testid="melody-analysis"]')
    };

    const analysisElement = analysisMap[type];
    await expect(analysisElement).toBeVisible({ timeout: 5000 });
  }

  async expectRomanNumerals(expectedNumerals: string[]) {
    for (const numeral of expectedNumerals) {
      await expect(this.romanNumerals).toContainText(numeral);
    }
  }

  async expectKeyCenter(expectedKey: string) {
    await expect(this.keyCenter).toContainText(expectedKey);
  }

  async expectMode(expectedMode: string) {
    await expect(this.modeDisplay).toContainText(expectedMode);
  }

  async expectConfidenceRange(type: 'functional' | 'modal' | 'chromatic', minConfidence: number, maxConfidence: number) {
    const confidenceElement = this.page.locator(`[data-testid="${type}-confidence"]`);
    const confidenceText = await confidenceElement.textContent();
    const confidence = parseFloat(confidenceText?.replace(/[^\d.]/g, '') || '0');

    expect(confidence).toBeGreaterThanOrEqual(minConfidence);
    expect(confidence).toBeLessThanOrEqual(maxConfidence);
  }

  async expectUIElements(expectedElements: string[]) {
    for (const elementSelector of expectedElements) {
      const element = this.page.locator(elementSelector);
      await expect(element).toBeVisible({ timeout: 5000 });
    }
  }

  async expectNoErrors() {
    await expect(this.errorMessage).not.toBeVisible();
  }

  async clearInput() {
    await this.clearButton.click();
    await expect(this.chordProgressionInput).toHaveValue('');
    await expect(this.resultsPanel).not.toBeVisible();
  }

  // Interaction testing methods
  async testButtonInteraction(buttonSelector: string, expectedAction: string) {
    const button = this.page.locator(buttonSelector);
    await expect(button).toBeVisible();
    await expect(button).toBeEnabled();
    await button.click();

    // Verify button press had expected effect
    if (expectedAction === 'clear') {
      await expect(this.chordProgressionInput).toHaveValue('');
    } else if (expectedAction === 'analyze') {
      await this.waitForAnalysisComplete();
    }
  }

  async testInputInteraction() {
    // Test typing
    await this.chordProgressionInput.click();
    await this.chordProgressionInput.type('C F G');
    await expect(this.chordProgressionInput).toHaveValue('C F G');

    // Test selection
    await this.chordProgressionInput.selectText();
    await this.chordProgressionInput.type('Am F C G');
    await expect(this.chordProgressionInput).toHaveValue('Am F C G');

    // Test clearing
    await this.chordProgressionInput.clear();
    await expect(this.chordProgressionInput).toHaveValue('');
  }

  async testModalInteraction(modalTriggerSelector: string) {
    const modalTrigger = this.page.locator(modalTriggerSelector);
    await modalTrigger.click();

    // Check modal appears
    const modal = this.page.locator('[role="dialog"]');
    await expect(modal).toBeVisible();

    // Check modal can be closed (ESC key)
    await this.page.keyboard.press('Escape');
    await expect(modal).not.toBeVisible();

    // Check modal can be closed (close button)
    await modalTrigger.click();
    await expect(modal).toBeVisible();

    const closeButton = modal.locator('[data-testid="close-button"]');
    if (await closeButton.isVisible()) {
      await closeButton.click();
      await expect(modal).not.toBeVisible();
    }
  }

  async testNavigationInteraction() {
    // Test tab navigation
    if (await this.analysisHubTab.isVisible()) {
      await this.analysisHubTab.click();
      await expect(this.page.locator('[data-testid="analysis-hub-content"]')).toBeVisible();
    }

    if (await this.scaleFinderTab.isVisible()) {
      await this.scaleFinderTab.click();
      await expect(this.page.locator('[data-testid="scale-finder-content"]')).toBeVisible();
    }
  }
}
