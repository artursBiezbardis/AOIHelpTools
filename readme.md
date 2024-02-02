
# Description

### This application has three tools, that eases work with cyberOptics AOI.
#### 1. Compare Mash - is for comparing two different mash files. This tool just outputs differences in components, this helps create new AOI recipe from existing recipes.
#### 2. Find Recipes by Part  - allows two find all recipes where specific part is located and then update part in all recipes using part template from library, this helps when for some part is detected wrong AOI template settings, you don't need to search for part in every recipe and update it manually.
#### 3. Group Components - allows to separate components, from others, by drawing area around components where separation is needed. For example this helps in situation where component pads are different from for same parts, in some cases there is up to 1000 components, where each component needs to be separated manually.
#### 4. Compare Mash And Recipe - Compares mash and recipe components if there is differencis in component part name or its dosn't exist in recipe or mash, differencis is visable in list. And if there is differencis, with update button you can update recipe from mash data (this feature is under development in updateRecipeAfterCompareMashRecipe branch)

# Installation

* from cmd or terminal navigate location to download
* run `git clone git@github.com:artursBiezbardis/AOIHelpTools.git`
* install `Python3.11`
* navigate to root
* run `pip install -r requirements.txt`
* run `python main.py`
