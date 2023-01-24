# Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

## Types of Contributions


### Report Bugs

Report bugs at https://github.com/ACTRIS-CCRES/ccres-weather-station/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

### Write Documentation

CCRES Weather Station could always use more documentation, whether as part of the
official CCRES Weather Station docs, in docstrings, or even on the web in blog posts,
articles, and such.

### Submit Feedback

The best way to send feedback is to file an issue at https://github.com/ACTRIS-CCRES/ccres-weather-station/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

## Get Started!

Ready to contribute? Here's how to set up `ccres_weather_station` for local development.

1. Fork the `ccres_weather_station` repo on GitHub.
2. Clone your fork locally:

    $ git clone git@github.com:your_name_here/ccres_weather_station.git

3. Install your local copy into a virtual environment.
   1. With **`venv`** : Assuming you have `venv` installed, this is how you set up your fork for local development :

    ```
    cd ccres_weather_station/
    python -m venv <name_of_your_env>
    pip install -e .[dev]
    ```

    2. With **`conda`** : Assuming you have conda installed, this is how you set up your fork for local development :

    ```
    cd ccres_weather_station/
    conda create -n <name_of_your_env> python=3.10
    conda activate <name_of_your_env>
    pip install -e .[dev]
    ```

4. Install the pre-commit hooks by running :
    ```
    pre-commit install
    ```

5. Make sure you have `git-lfs` installed, then run `git lfs install`.

6. Create a branch for local development:

    ```
    git checkout -b name-of-your-bugfix-or-feature
    ```

   Now you can make your changes locally.

7. When you're done making changes, apply the pre-commit and check that your changes pass the
   tests, including testing other Python versions.

    ```
    pre-commit ccres_weather_station tests
    python -m pytest
    ```

8. If files are modified by the pre-commit hooks, you need to rea-add them :
    ```
    git add <your-modified-files>
    ```

9. Commit your changes and push your branch to GitHub:

    ```
    git add .
    git commit -m "Your detailed description of your changes."
    git push origin name-of-your-bugfix-or-feature
    ```

10.  Submit a pull request through the GitHub website.

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 3.5, 3.6, 3.7 and 3.8, and for PyPy. Check
   https://github.com/ACTRIS-CCRES/ccres-weather-station/pull_requests
   and make sure that the tests pass for all supported Python versions.

## Tips

To run a subset of tests :
```
python -m pytest tests.test_ccres_weather_station
```
## Deploying

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed (including an entry in HISTORY.rst).
Then run:

```
bump2version patch # possible: major / minor / patch / release_candidate / dev
git push
git push --tags
```

This will then deploy the package in PyPI if tests pass and a tag is set,
otherwise it will deployed on test-pipy.

## Further words

### `pre-commit`

Most of the pre-commit hooks require you to do nothing but save the changes. However, some pre-commits (e.g. `pydocstyle`) are sometimes hard to respect and can slow down your workflow. Although we recommend to let all of them to have a cleaner repo, if one or more are really annoying for you, you can remove or comment them in the `.pre-commit-config.yaml` file.

Before each commit, each hook is going to run against file in the staged area (files added with `git add`). Some of the hooks may modify the files, if this happened, the commit is cancelled. You need to re-add the file(s) modified by running `git add <modified-file>` and recommit.

### Conventional commits

Although it is not mandatory, we suggest you to use the [Conventional Commit](https://www.conventionalcommits.org/en/v1.0.0/) conventions to write commit messages.
