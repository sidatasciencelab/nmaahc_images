# NMAAHC Images

To set up the correct conda environment for this project do this:

```
conda env create -f environment.yml
```

This will install all of the required Python libraries, but you will need to set up two Environment Variables in order to use the EDAN API. Either apply for EDAN credentials at https://edandoc.si.edu/request-credentials, or contact Mike for the OCIO Data Science lab credentials. Then follow the OS-specific instructions at https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#saving-environment-variables to add these variables to your conda activation and deactivation steps.

This will create a conda environment called *nmaahc_images*. You will need to run `conda activate nmaahc_images` in order to "activate" this environment.
