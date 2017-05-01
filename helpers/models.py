import os
import re
def best_model(model_dir, model_name):
    best_model_name = None
    highest_accuracy = -1
    for current_model_name in os.listdir(model_dir):
        if not model_name in current_model_name:
            continue # other files are also stored in that dir
        model_accuracy = float(re.search("\-acc[0-9]\.[0-9]{3}",current_model_name).group(0)[4:])
        if model_accuracy>highest_accuracy:
            highest_accuracy = model_accuracy
            best_model_name=current_model_name
    if best_model_name == None:
        raise ValueError("No model(%s) found in (%s). Please run training first. "%(model_dir, model_name))
    return os.path.join(model_dir, best_model_name)
