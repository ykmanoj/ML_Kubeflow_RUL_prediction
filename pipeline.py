import kfp
from kfp import dsl
from kfp.components import func_to_container_op

@func_to_container_op
def show_results(nn : float, lr : float, rf:float) -> None:
    # Given the outputs from Neural Network, logistic regression and Randomforest components
    # the results are shown.

    print(f"Neural Network (accuracy): {nn}")
    print(f"Logistic regression (accuracy): {lr}")
    print(f"RandomForest regression (accuracy): {rf}")


@dsl.pipeline(name='Turbofan Engine Pipeline', description=' Apply LSTM to find Remaining useful life.')
def rul_pipeline():

    # Loads the yaml manifest for each component
    collect_data = kfp.components.load_component_from_file('./data/extract_data.yaml')
    processed_data = kfp.components.load_component_from_file('./preprocess/process_data.yaml')
    #nn = kfp.components.load_component_from_file('nn/nn_regressor.yaml')
    lr = kfp.components.load_component_from_file('lr/logistic_regression.yaml')
    rf = kfp.components.load_component_from_file('rf/rf_classifier.yaml')

    # Run download_data task
    download_task = collect_data()
    preprocess_data = processed_data(download_task.output)

    # Run tasks "random_forest" and "logistic_regression"
    #nn_task = nn(preprocess_data.output)
    lr_task = lr(preprocess_data.output)
    rf_task = rf(preprocess_data.output)

    # Given the outputs from "random_forest" and "logistic_regression"
    # the component "show_results" is called to print the results.
    show_results(rf_task.output, lr_task.output)


if __name__ == '__main__':
    kfp.compiler.Compiler().compile(rul_pipeline, 'RUL.yaml')
    client = kfp.Client(host='https://3e442dc890e9f588-dot-us-central1.pipelines.googleusercontent.com')
    client.create_run_from_pipeline_func(rul_pipeline, arguments={})
