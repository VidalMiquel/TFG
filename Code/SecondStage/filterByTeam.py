from decimal import DivisionByZero
import sys
import os
import json
import pandas as pd


# Function to get command-line parameters
def getParameters():
    if len(sys.argv) == 3:
        return sys.argv[1], sys.argv[2]
    else:
        print("Exactly two values must be provided as arguments.")
        sys.exit(1)


# Function to generate dynamic paths for data and target folders
def generateDynamicPaths(experimentName):
    currentDir = os.path.abspath(
        os.path.dirname(__file__)
    )  # Get the current directory of the script
    print(currentDir)
    dataFolder = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "SecondStage", "Middle_files"
    )
    print(dataFolder)
    targetFolder = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "SecondStage", "Target_files"
    )
    print(targetFolder)

    if not os.path.exists(targetFolder):
        print(
            f"The folder {targetFolder} does not exist for experiment {experimentName}."
        )
        sys.exit(1)

    return dataFolder, targetFolder


# Function to filter data based on possession team
def filterFileByPossessionTeam(data, nameClub):
    # Filter rows based on conditions
    dataTeam = data[data["possession_team"].apply(lambda x: (x)["name"] == nameClub)]

    # Check if 'dataTeam' is not empty before proceeding
    if not dataTeam.empty:
        return dataTeam
    else:
        return None


# Function to save filtered data to a file
def saveFilteredFile(data, targetFolder, fileName):
    # Check if the segment is not empty before saving
    if not data.empty:
        # File name in the format Football_day_n_m
        newFileName = changeFilenames(fileName)
        filePath = os.path.join(targetFolder, newFileName)
        try:
            data.to_json(filePath, orient="records", lines=True)
            print(f"File stored at: {filePath}")
        except Exception as e:
            print(f"Error while saving the file: {e}")
        #print(f"File '{newFileName}' generated successfully.")
    else:
        print(f"The file is empty, no file will be generated.")


# Function to read files in a folder and process them
def readFolderFiles(currentPath, targetFolder, nameClub):
    # Check if the folder exists
    if not os.path.isdir(currentPath):
        print(f"The folder '{currentPath}' does not exist.")
        return

    # Iterate through all the files in the folder
    for fileName in os.listdir(currentPath):
        # Join the folder path with the file name
        filePath = os.path.join(currentPath, fileName)

        try:
            with open(filePath, "r", encoding="utf-8") as file:
                content = json.load(file)
                dFrame = pd.DataFrame(content)
                filteredData = filterFileByPossessionTeam(dFrame, nameClub)
                saveFilteredFile(filteredData, targetFolder, fileName)
        except OSError as e:
            print(f"Error while reading the file '{fileName}': {e}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in '{fileName}': {e}")


# Function to change file names to a new format
def changeFilenames(fileName):
    # Check if the file name follows the pattern "Football_day_{jornada_value}_{i+1}.json"
    if fileName.startswith("footballDay_") and fileName.endswith(".json"):
        partsName = fileName.split("_")
        jornadaValue = partsName[1]
        iValue = partsName[2].split(".")[0]

        # New file name
        newFileName = f"footballDayFiltered_{jornadaValue}_{iValue}.json"
        return newFileName


# Main function to execute the program
def main():
    experimentName, clubName = getParameters()
    dataFolder, targetFolder = generateDynamicPaths(experimentName)
    readFolderFiles(dataFolder, targetFolder, clubName)


if __name__ == "__main__":
    main()
