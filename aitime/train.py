import tensorflow as tf
import random

class KFoldTrainer(object):

    def __init__(self, dataPool, batch_size=50):
        self.dataPool = dataPool
        self.batch_size = batch_size

        # Use the size of the first sequence in first dataset to set this automatically
        self.model = dense_model()

    def train_and_evaluate(self):
        self.train_fold(0)

    def train_fold(self, fold):

        # Let's make sure to shuffle thoroughly
        ds = [a for a in self.dataPool.datasets[0].iter_all()]
        random.shuffle(ds)

        # We'll need to optimize these later - making them simple for now
        x_train = [a[0] for a in ds]
        y_train = [a[1] for a in ds]

        self.model.compile(optimizer='adam', loss=tf.keras.losses.BinaryCrossentropy(), metrics=['accuracy'])
        self.model.fit(x_train, y_train, epochs=5)



def dense_model():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(100),
        tf.keras.layers.Dense(100),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    return model
