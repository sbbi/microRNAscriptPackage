from sys import argv
import os
import math
from random import sample as ssample
from random import shuffle
from datetime import datetime

class Main():
    def __init__(self):

        kingdomSelection = argv[1]
        featureStart = int(float(argv[2]))
        featureEnd = int(float(argv[3]))
        ##
        ## Generate Datasets
        ##
        #Define Files
        pFile = "datasets2/"+kingdomSelection+"_data_new_positive.txt"
        nFile = "datasets2/"+kingdomSelection+"_data_new_negative.txt"

        #Read Files
        positive_dataset = readFiles(pFile)
        negative_dataset = readFiles(nFile)

        ranking = []
        """
        with open("step3/%s/%s.fscore"%(kingdomSelection, kingdomSelection)) as f:
            for lin in f:
                line = lin.strip()
                sp = line.split(':')
                ranking.append(int(float(sp[0])))
        """

        print "%d rows in %s" % (len(positive_dataset), pFile)
        print "%d rows in %s" % (len(negative_dataset), nFile)
        print "Total rows: %s" % (len(positive_dataset) + len(negative_dataset))
        print "Ranking contains %d" % len(ranking)

        positive_samples, negative_samples = generateSamples(positive_dataset, negative_dataset)
        training_set, testing_set = generateTrainingAndTestingSets(positive_samples, negative_samples)

        print "Training Set: %s" % len(training_set[0])
        print "Testing Set: %s" % len(testing_set[0])

        gen = xrange(featureStart,featureEnd,1)

        for i in gen:
            without = ranking[i:]
            without = set(without)
            convert_to_libsvm_format(training_set[0], 'step3/%s/%s.all.libsvm'%(kingdomSelection,kingdomSelection), without)
            #convert_to_libsvm_format(testing_set[0], 'step3/%s/%s.te.libsvm'%(kingdomSelection,kingdomSelection), without)

def readFiles(fil):
    """
    @Param files to read
    :return: A 2x2 matrix, Each row is a miRNA, Each column is a feature
    """
    print "Reading %s" % fil
    outArray = []
    with open(fil) as f:
        for lin in f:
            line = lin.strip()
            sp = line.split(',')
            outArray.append(sp)
    #del outArray[0] #Remove Header
    return outArray

def readSVM(fil):
    label = []
    samples = []
    with open(fil) as f:
        for line in f:
            sp = line.strip().split()
            label.append(int(sp[0]))
            aDict = dict()
            for feature in sp[1:]:
                spp = feature.split(':')
                aDict[int(spp[0])] = float(spp[1])
            samples.append(aDict)
    return label, samples


def generateSamples(positive_dataset, negative_dataset):
    """

    :return: 30 positive and negative datasets
    """
    positive_samples = []
    negative_samples = []
    num_samples = int(math.ceil(float(len(positive_dataset))*.80))
    if num_samples % 2 == 1:
        num_samples += 1

    print "Generating %s samples" % (num_samples)
    for i in xrange(0, 1):
        positive_samples.append(ssample(positive_dataset, num_samples))
        negative_samples.append(ssample(negative_dataset, num_samples))

    print len(negative_samples[0]), len(positive_samples[0])
    return positive_samples, negative_samples


def convert_to_libsvm_format(array2d, file_name, exclude):
    print "Converting to LibSVM"
    f = open(file_name, 'w')
    for row in array2d:
        line = ''
        i = 0
        skipped = 1
        for column in row:
            #if i == 0:
            #    i += 1
            #    continue
            if i == 0:
                try:
                    line += '%s ' % int(float(column))
                except TypeError as e:
                    print column
                    g = open('tmp/error.txt','w')
                    g.write("%d\n"%i)
                    g.write(e.message+'\n')
                    g.write(str(e.args)+'\n')
                    for rrr in column:
                        g.write(str(rrr)+'\n')
                    g.close()
                    exit()
                i += 1
            else:
                if (i-1) in exclude:
                    skipped += 1
                else:
                    line += '%d:%f ' % (i+1-skipped, float(column))
                i += 1
        #print "Skipped", i
        f.write(line+'\n')
    f.close()

def generateTrainingAndTestingSets(positive_samples, negative_samples):
    """

    :param positive_samples:
    :param negative_samples:
    :return: samples for training and testing
    """
    print "Generating Training/Testing Sets from %s positive samples and %s negative samples" % (len(positive_samples), len(negative_samples))
    samples_for_training = []
    samples_for_testing = []
    for i in xrange(len(positive_samples)):
        print "loop %s" % i
        half = int(math.ceil(len(positive_samples[0])))
        shuffle(positive_samples[i])
        shuffle(negative_samples[i])
        pos_train = positive_samples[i][:half]
        pos_test = positive_samples[i][half:]
        neg_train = negative_samples[i][:half]
        neg_test = negative_samples[i][half:]

        pos_train.extend(neg_train)
        pos_test.extend(neg_test)


        samples_for_training.append(pos_train)
        samples_for_testing.append(pos_test)
    return samples_for_training, samples_for_testing

if __name__ == '__main__':
    ne = Main()