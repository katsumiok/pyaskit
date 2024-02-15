# Contributing to *AskIt*

First off, thank you for considering contributing to AskIt. It's people like you that make AskIt such a great tool.

Following these guidelines helps to communicate that you respect the time of the developers managing and developing this open source project. In return, they should reciprocate that respect in addressing your issue, assessing changes, and helping you finalize your pull requests.

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report for AskIt. Following these guidelines helps maintainers and the community understand your report, reproduce the behavior and find related reports.

- Use the GitHub issue tracker to report bugs.
- Before submitting a bug report, please check if a similar issue has already been reported. If there is, please add any more information that you have, it might be very helpful.
- Be as detailed as possible. All the details provided will help us understand more about the problem and fix it faster.

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for AskIt, including completely new features and minor improvements to existing functionality.

- Use the GitHub issue tracker to suggest enhancements.
- Provide as many details as possible in your issue.

### Pull Requests

- Fork the project, create a new branch, make your changes, and create a pull request. 

## Setup for Local Development

- First, fork the AskIt repo on GitHub.
- Clone your fork locally:

```bash
git clone git@github.com:katsumiok/py_askit.git
```


- Install the development requirements:

```bash
pip install -r requirements_dev.txt
```

- Create a branch for local development:

```bash
git checkout -b name-of-your-bugfix-or-feature
```

- Make your changes locally.
- When you're done making changes, check that your changes pass flake8 and the tests:

```bash
black pyaskit tests
mypy pyaskit tests
pytest
```

- Commit your changes and push your branch to GitHub:

```bash
git add .
git commit -m "Your detailed description of your changes."
git push origin name-of-your-bugfix-or-feature
```

- Submit a pull request through the GitHub website.

## Project Setup

XXX: Add project setup instructions here.

## Code Review

<!--
Look for the GitHub's pull request page after you push your changes. Click the `Reviewers` dropdown and select the person or team you want to review your pull request.
>

## PR Approval

We review Pull Requests on a regular basis. We will provide feedback if any changes are needed. If the PR is approved, we will merge your changes.

Again, thank you for your contribution!
