# PreGit: Git Merge Using AI to Resolve Conflicts

## Warning 🚧

This repository is a base for an old research project.
You can use it as a starting point, but it will not work out of the box.

I'm releasing it as open source, because I think it could be useful for someone who wants to start a similar project. (I'm not planning to work on it anymore, even though I think it's a cool idea.)

## Introduction

The goal is to recreate the diff patch method: we provide a source code, a patch and we need to predict the resulting code.
Lost of git conflicts are avoidable, but the current merge tools are not able to predict the resulting code.
The goal is to use a neural network to predict the resulting code.

## Schema

### Option A

```
     VariantA
    /         \
Source         Destination
    \         /
     VariantB
```

-   Model input
    -   Source
    -   PatchA (VariantA - Source)
    -   PatchB (VariantB - Source)
-   Model output
    -   Destination

In a clean way, we should provide the model with the source code, two variants and learn to predict the destination code.
However:

1. This can be a bit tricky because files can be quite large (and model don't handle large context).
2. This mean we will replace the default merge tool, which can be (a) dangerous and (b) expensive / slow

### Option B

Another way then, is to provide the model with the source code, and the conflict (the diff patch).

```
     VariantA
    /         \
Source         Diff -> Destination
    \         /
     VariantB
```

-   Model input
    -   Source
    -   Diff (VariantA - VariantB)
-   Model output
    -   Destination

## Use

### Database Schema

-   `repository` git repositories
-   `merge`: unused. model for the option A
-   `commit_file`: model for the option B

### Code Structure

-   `diff.py` - usuned. code to detech and extract conflict information from git merge
-   `download.py` - download public repositories from github
-   `model.py` - sqlalchemy model
-   `repository.py` - helper around git repository
-   `parse_commit.py` - parse repository and extract commit from merge commit

### Install

1. `pip install -r requirements.txt`
2. Create PG Database `pregit`
3. Create model `python model.py`

### Run

1. `python download.py`: download the most popular repositories
2. `python parse.py`: parse ????
3. `python parse_commit.py`: parse the repositories to get "transactions" data.

## TODO

If you want to work on this project, I think the next steps are:

-   [ ] Clean code
-   [ ] Add a way to target the code of the "source" and "destination" to use for a specific git conflict.
-   [ ] Train using LLM
-   [ ] Profit $$$

### Train using LLM (GPT3 / Codex / etc)

Prompt

````
Source

```python
    def common_module_test(self, app):
        assert app.secret_key == 'devkey'
        assert app.config['TEST_KEY'] == 'foo'
```
Diff A
```python
    def common_object_test(self, app):
        assert app.secret_key == 'devkey'
        assert app.config['TEST_KEY'] == 'foo'
```
Diff B
```python
    def common_module_test(self, app):
        assert app.secret_key == 'devkey'
        assert app.config['test_key'] == 'foo'
```

# Predict the git conflict resolution
Destination
````

Output

````
```
    def common_object_test(self, app):
        assert app.secret_key == 'devkey'
        assert app.config['test_key'] == 'foo'
```
````
