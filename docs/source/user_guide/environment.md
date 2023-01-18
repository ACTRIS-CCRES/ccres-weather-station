# Set up development environment

```shell
pip install -f requirements_dev.txt
```

## `pre-commit`
Before a commit and after staging changes you have to run the following command :

```
pre-commit
```

It will makes changes on staged files such as remove trailing whitespace, reformat etc.
You can also install pre-commit in order to apply this command when you enter `git commit` command. To do so :

```
pre-commit install
```

If after a commit you see that a stage has failed (such as black) you add to restage it with `git add <changed_file(s)>`
