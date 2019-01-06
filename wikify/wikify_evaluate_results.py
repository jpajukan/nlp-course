import sys

def main(correctResultsFile, resultsToEvaluateFile):
    amount_correct=0
    amount_total=0
    trash = correctResultsFile.readline() # read the headers
    trash = resultsToEvaluateFile.readline()
    while(True):
        line_correct = correctResultsFile.readline()
        if line_correct == "": #if we've reached EOF
            break
        line_correct = line_correct.split(", ")
        url_correct = line_correct[2].strip()
        #print(url_correct)
        #input()
        
        line_result = resultsToEvaluateFile.readline()
        if line_result == "":
            break
        line_result = line_result.split(", ")
        #print(line_result)
        #input()
        try:
            url_result = line_result[2].strip()
        except:
            print(line_result)
            exit
        #print(url_result)
        #input()
        
        amount_total = amount_total + 1.0
        if url_correct == url_result:
            amount_correct = amount_correct + 1.0
    #print(amount_total)
    #print(amount_correct)
    print("The accuracy for", resultsToEvaluateFile.name, "is:", amount_correct/amount_total)
        

if __name__ == "__main__":
    usage = 'wikify_evaluate_results.py fileWithCorrectResults fileWithResultsToEvaluate'
    if len(sys.argv) != 3:
        print(usage)
        sys.exit(1)
    try:
        with open(sys.argv[1], 'r') as f1:
            with open(sys.argv[2], 'r') as f2:
                main(f1, f2)
    except FileNotFoundError:
        print('File(s) not found')