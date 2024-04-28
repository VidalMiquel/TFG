import os
import sys

def getExperimentName():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        return None

def createFolderStructure(stageName, experimentName):
    # Function to create folder if it doesn't exist
    def createFolder(path):
        try:
            os.makedirs(path)
        except FileExistsError:
            pass

    # Get the absolute path of the current directory
    currentPath = os.path.abspath(os.path.dirname(__file__))

    # Construct the absolute path for the folders
    folderPath = os.path.join(currentPath, "..", "..", "Data", experimentName, stageName)

    # Create the folders based on stage name
    if stageName != "04Stage" and stageName != "05Stage" and stageName != "00Stage":
        createFolder(os.path.join(folderPath, "MiddleFiles"))
        createFolder(os.path.join(folderPath, "TargetFiles"))
    elif stageName == "04Stage":
        createFolder(os.path.join(folderPath, "Graphs"))
        createFolder(os.path.join(folderPath, "Graphs", "diGraphs"))
        createFolder(os.path.join(folderPath, "Graphs", "multiDiGraphs"))
        createFolder(os.path.join(folderPath, "Graphics"))
        createFolder(os.path.join(folderPath, "Metrics"))
        createFolder(os.path.join(folderPath, "Metrics", "Individual"))
        createFolder(os.path.join(folderPath, "Metrics", "Global"))
    elif stageName == "05Stage":
        createFolder(os.path.join(folderPath, "Tables", "Individual"))
        createFolder(os.path.join(folderPath, "Tables", "Global"))
    else:
        pass

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python scriptName.py experimentName stageName")
        sys.exit(1)

    experimentName = sys.argv[1]
    stageName = sys.argv[2]

    if not stageName:
        print("No stage name provided.")
        sys.exit(1)
    else:
        createFolderStructure(stageName, experimentName)
