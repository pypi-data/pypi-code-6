import pydecode
import pydecode.model
import numpy as np

# class IDStructuredCoder(object):
#     def inverse_transform(self, outputs):
#         return outputs

#     def transform(self, y):
#         return y

# class TestFeatures(pydecode.model.StructuredFeatures):
#     @property
#     def feature_templates(self):
#         return [(10, 100), (10)]

#     def output_features(self, x, outputs):
#         return [(outputs[:,0], outputs[:,1]),
#                 (outputs[:,0],)]


# X = ["one", "two"]
# Y = [np.array([(0, 1)]), np.array([(1, 10)])]

# def _test_features():
#     struct_features = TestFeatures(IDStructuredCoder())
#     struct_features.initialize(X, Y)
#     features = struct_features.joint_features("three", np.array([(1, 1)]))
#     features2 = struct_features.joint_features("four", np.array([(1, 2)]))

#     print features
#     print features2

#     # These two should have the different values for the first feature
#     # These two should have the same value for the second feature.
#     assert len((features2 - features).nonzero()) == 2


#     matrix = struct_features.feature_matrix("five", np.array([(0, 0), (1, 2), (3, 3)]))



# class TestPreprocessor(pydecode.model.LabelPreprocessor):

#     def input_labels(self, x):
#         labels = []
#         for xe in x:
#             labels.append([xe, xe[:3], xe[-3:], xe[0].isupper()])
#         return np.array(labels).T

# def _test_preprocess():
#     X = [np.array("a dog there is".split()),
#          np.array("two no one knows here".split())]
#     preprocess = TestPreprocessor()
#     preprocess.initialize(X)

#     preprocess.preprocess("a dog knows hereeee".split())


# class TestDPModel(pydecode.model.DynamicProgrammingModel):

#     def dynamic_program(self, x):
#         items = np.arange(10)
#         out = np.arange(10 * 10).reshape(10, 10)
#         c = pydecode.ChartBuilder(items, out)
#         c.init(items[:2])
#         c.set(items[3],
#               items[:2],
#               out=np.array([out[0,0], out[1,1]]))
#         return c.finish()

# def _test_dp_model():
#     model = TestDPModel(IDStructuredCoder(),
#                         TestFeatures(IDStructuredCoder()))
#     model.initialize(X, Y)
#     w = np.zeros(model.size_joint_feature)
#     model.argmax(X[0], w)
