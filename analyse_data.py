def analyse_data():
    elif dataset == "cmapss":
        training_data, testing_data, training_pd, testing_pd = get_CMAPSSData(save=True, files=files,
                                                                              min_max_norm=min_max)
        x_train = training_data[:, :training_data.shape[1] - 1]
        y_train = training_data[:, training_data.shape[1] - 1]
        print("training", x_train.shape, y_train.shape)

        x_test = testing_data[:, :testing_data.shape[1] - 1]
        y_test = testing_data[:, testing_data.shape[1] - 1]
        print("testing", x_test.shape, y_test.shape)

        if plot:
            plt.plot(y_train, label="train")
            plt.figure()
            plt.plot(y_test, label="test")

            plt.figure()
            plt.plot(x_train)
            plt.title("train: FD00" + str(files[0]))
            plt.figure()
            plt.plot(y_train)
            plt.title("train: FD00" + str(files[0]))
            plt.show()