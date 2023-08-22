# Axiom - The Fact Checking Browser Extension

The vision of Axiom is to be a cross-platform browser extension that reads news articles and provides online fact checking. It does so by first, highlighting key sentences and then providing links to and context from primary sources that either verify or oppose the statement.

The task is daunting and has many challenges to it (most revolving around ground truth, bias, opinion, etc). However, the early stages of the project should be a useful rampup in exploring some basic LLM text comprehension tasks.

## Milestones
### Summary
* [X] Milestone 0 - Create a Chrome extension that hightlights the workd "the" on every page `extension`
* [ ] Milestone 1 - Make Chrome extension cross-platform `extension/js`
* [ ] Milestone 2 - Highlight sentences/phrases that summarize a news article `llm/js`
* [ ] Milestone 3 - Summarize an abstract of the article when clicking on the headline `llm`
* [ ] Milestone 4 - Determine sentences that need to be fact checked with a classification model `ml`
* [ ] Milestone 5 - Highlight and provide a "dummy" popup response for fact-checkable sentences `js/css`
* [ ] Milestone 6 - Assess strategies for building a knowledge graph and querying it based on highlighted sentences
  * This is likely to be very complex and should be a whole other project that consists of:
    * web crawling for new knowledge
    * data storage/representation/querying/serving

## Installation
Download or clone this repository to your local machine.

### Chrome
1. Navigate to the browser's extension settings: `chrome://extensions/`
3. Enable "Developer Mode" in the top-right corner
4. Click on "Load Unpacked" and select the `axiom/src` directory

## Usage

## Known Issues

## Contributing
This repo is primarily maintained by [Gregg Tabot](mailto:gregg.tabot@snyaptiq.ai), but contributions are welcome!

If you encounter any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.