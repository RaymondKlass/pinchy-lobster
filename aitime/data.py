import random


# Setup a consistent random seed - could be any number as long as it's consistent
random.seed(10)

class DataPool(object):

    def __init__(self, numSamples=1000):
        self.numSamples = numSamples

    def extract_sequences(self, sequence_length=100):
        """
        For this method we take the input for number of sample and actually create the samples
        :return:
        """

        self.pool = [DataSequence.from_ordering(i%2, sequence_length) for i in range(self.numSamples)]

    def extract_windows(self, window_length=10):
        """
        Extract windows using the data sequence - sequential splitter
        :return:
        """
        for ds in self.pool:
            ds.split_windows(window_length)


    def split_pool(self, k):
        """
        Split the data Pool into k datasets - representing folds, going to initially split with whole DataSequences
        in the same dataset
        :param folds:
        :return:
        """

        # We should be checking to make sure that k < len(self.pool)

        self.datasets = [Dataset()] * k
        for  i, ds in enumerate(self.pool):
            self.datasets[i % k].data_sequences.append(ds)

    def augment_pool(self, factor=10):
        """
        Save an augmented version of each dataset so that we can use it during training
        :return:
        """

        for ds in self.datasets:
            ds.save_augmented_version(factor)


    def extract_features(self):
        """
        Going to pass on the logic for this one (I'll pipe it through, but it won't do a transformation yet)
        :return:
        """

        for ds in self.datasets:
            ds.extract_features()




class Dataset(object):

    def __init__(self, data_sequences=[]):
        self.data_sequences = data_sequences

    def save_augmented_version(self, factor):

        for ds in self.data_sequences:
            ds.augment(factor)

    def extract_features(self):
        for ds in self.data_sequences:
            ds.extract_features()

    def __iter__(self):
        for ds in self.data_sequences:
            for seq in ds:
                yield seq

    def iter_all(self):
        for ds in self.data_sequences:
            for seq in ds.iter_all():
                yield seq



class DataSequence(object):

    def __init__(self, sequence, ordering):
        """
        The ordering is the annotation. 0 for decreasing, 1 for increasing
        :param sequence:
        :param ordering:
        """
        self.sequence = sequence
        self.sub_sequences = []
        self.aug_sub_sequences = []
        self.ordering = round(ordering)


    def __iter__(self):
        for seq in self.sub_sequences:
            yield (seq, self.ordering)


    def __len__(self):
        return len(self.sub_sequences)

    def iter_all(self):

        for seq in self.sub_sequences:
            yield (seq, self.ordering)

        for seq in self.aug_sub_sequences:
            yield (seq, self.ordering)

    def len_all(self):
        return len(self.aug_sub_sequences) + len(self.sub_sequences)


    def split_windows(self, window_length):
        """
        To avoid any issues with different sequence size, we'll only store whole sequences
        :param window_length: int
        :return:
        """

        # Split into sequential windows of equal length
        self.sub_sequences = [[]]*(len(self.sequence) // window_length)
        for i in range(len(self.sub_sequences)):
            self.sub_sequences[i] = self.sequence[i*window_length:(i*window_length)+window_length]


    def augment(self, factor):
        """
        Increase data size and save them as augmented sequences - so they can be treated differently when evaluating
        :param factor:
        :return:
        """
        self.aug_sub_sequences = []
        for seq in self.sub_sequences:
            for i in range(factor):
                mul = random.randrange(0, 500)
                self.aug_sub_sequences.append([a*mul for a in seq])


    def extract_features(self):
        """
        Extract features from both the sub_sequences and the Augmented sequences
        :return:
        """
        for i in range(len(self.sub_sequences)):
            self.sub_sequences[i] = self.extract_sequence_featue(self.sub_sequences[i])

        for i in range(len(self.aug_sub_sequences)):
            self.aug_sub_sequences[i] = self.extract_sequence_featue(self.aug_sub_sequences[i])


    def extract_sequence_featue(self, sequence):
        return sequence


    @classmethod
    def from_ordering(cls, ordering, length, base=None):
        """
        Create a Data Sequence from an ordering and a length
        :param ordering:
        :return:
        """

        # add a random base to the sequences to add variation
        if not base:
            base = random.randint(0, 5000)

        # Increasing sequence
        if round(ordering):
            return cls([random.randrange(i+base, i+5+base) for i in range(length)], ordering)
        else: # Decreasing sequence
            return cls([random.randrange(length-i+base, length-i+5+base) for i in range(length)], ordering)

