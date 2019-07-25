from env.importing import OrderedDict
from io_.info_print import printing


def get_vocab_size_and_dictionary_per_task(tasks, pos_dictionary=None, type_dictionary=None, verbose=1):
    # TODO : should be factorize with load dictionaries
    if pos_dictionary is None and type_dictionary is None:
        assert "pos" not in tasks and "parsing" not in tasks, \
            "ERROR : pos or parsing are in tasks but related dictionaries are None"
        printing("INFO : no dictionaries and voc_sizes needed", verbose=verbose, verbose_level=1)
        return None, None
    num_labels_per_task = OrderedDict()
    task_to_label_dictionary = OrderedDict()

    if "pos" in tasks:
        assert pos_dictionary is not None
        task_to_label_dictionary["pos"] = pos_dictionary
        num_labels_per_task["pos"] = len(pos_dictionary.instance2index ) + 1
    if "parsing" in tasks:
        assert type_dictionary is not None
        num_labels_per_task["parsing_types"] = len(type_dictionary.instance2index) + 1
        num_labels_per_task["parsing_heads"] = 0
        task_to_label_dictionary["parsing_types"] = type_dictionary
        task_to_label_dictionary["parsing_heads"] = "index"

    return num_labels_per_task, task_to_label_dictionary