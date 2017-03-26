import os

from sklearn import svm
#import pickle
import joblib

from faceSpoofDetection import features

import dbfeatures
import feature_computer

# pickels filenames
saved_classifier_filename = '../classifiers/msu_mfsd.pkl'
saved_realfaces_features_filename = '../featuresVectors/msu_mfsd_realfaces_features_joblib.pkl'
saved_spooffaces_features_filename = '../featuresVectors/msu_mfsd_spooffaces_features_joblib.pkl'

# wheather to compute new features or load the features from saved files
load = False

# descriptor computer
mlbp_feature_computer = feature_computer.FrameFeatureComputer(features.MultiScaleLocalBinaryPatterns((8, 1), (24, 3),
                                                                                                    (40, 5)))
#mlbp_feature_computer = feature_computer.FrameFeatureComputer(features.LocalBinaryPatterns(8,1))


# compute feature vectors for every frame in the videos with real faces
if not load:
    real_features = dbfeatures.compute_face_features_msu_mfsd(mlbp_feature_computer, real=True)
    #with open(saved_realfaces_features_filename, 'w') as f:
        #pickle.dump(real_features, f)
    joblib.dump(real_features, saved_realfaces_features_filename)

    # compute feature vectors for every frame in the videos with spoof faces
    spoof_features = dbfeatures.compute_face_features_msu_mfsd(mlbp_feature_computer, real=False)
    #with open(saved_spooffaces_features_filename, 'w') as f:
    #    pickle.dump(spoof_features, f)
    joblib.dump(spoof_features, saved_spooffaces_features_filename)
else:
    #with open(saved_realfaces_features_filename, 'r') as f:
    #    real_features = pickle.load(f)
    real_features = joblib.load(saved_realfaces_features_filename)

    #with open(saved_spooffaces_features_filename, 'r') as f:
    #    spoof_features = pickle.load(f)
    spoof_features = joblib.load(saved_spooffaces_features_filename)

# create the necessary labels
labels_real = [1 for _ in range(len(real_features))]
labels_spoof = [0 for _ in range(len(spoof_features))]

# create the full features and corresponding labels
features = real_features + spoof_features
labels = labels_real + labels_spoof

clf = svm.SVC(gamma=0.07, verbose=True)
clf.fit(features, labels)

#joblib.dump(clf, saved_classifier_filename)
with open(saved_classifier_filename, 'w') as f:
    pickle.dump(clf, f)

from sklearn.metrics import accuracy_score

pred = clf.predict(features)

print(accuracy_score(labels, pred))
