# knr-auv/autonomy

knr-auv/autonomy is a software for the development of a behavioral tree-based autonomy module for the OKOŃ AUV built by KNR AUV team.

## Behavior Tree Editor

Behavioral tree projects placed in the BTs directory can be opened/edited using [the Behavior Tree Visual Editor](https://opensource.adobe.com/behavior_tree_editor).

## Creating Conda Environment with Dependencies (Python)

1. Create Conda Environment and Install Dependencies

    ```bash
    conda env create -f environment.yml
    ```

2. Activate Conda Environment

    ```bash
    conda activate okon-autonomy
    ```

## Updating Dependencies (Python)

1. Activate Conda Environment

    ```bash
    conda activate okon-autonomy
    ```

2. Update Conda Environment Dependencies

    ```bash
    conda env update -f environment.yml --prune
    ```
