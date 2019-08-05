
def sanity_check_early_stop_metric(early_stoppin_metric, task_parameter_setting, tasks):
    for task in tasks:
        for metrics in task_parameter_setting[task]["eval_metrics"]:
            test = (early_stoppin_metric in metrics)
            print(early_stoppin_metric, metrics, test)
            if test:
                break
        if test:
            break
    assert test, "ERROR : early_stoppin_metric {} not in task_parameter_setting tasks {} - {} ".format(early_stoppin_metric, tasks, task_parameter_setting)
