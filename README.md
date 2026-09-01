# allssh_tools
allssh tool that can be used across clusters

## Requirements
This works best with Visual Studio Code (VSCode) for ease of use and portability. Download the allssh_tools folder and use VSCode to open the folder as a new workspace. Then run main.py and follow the prompts from the terminal/CLI.

## Cluster Lists
By default, the list of Cohesity clusters is read from the shared_cohesity_clusters.txt file. If want to change the list/scope of the allssh.sh queries to hit select clusters update this file first and save it in your VSCode workspace.

## Intended Use
This tool is intended to have a menu system that allows you to choose different actions or behaviors. There will be options that have predetermined behaviors and their is a custom ALLSSH option to free run commands (please use this sparingly and only for mundane commands that show information to limit the scope of impact committed across the clusters).
