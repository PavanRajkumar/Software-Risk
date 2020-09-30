# Author: Richard Delwin Myloth, Pavan Rajkumar
# -*- coding: utf-8 -*-

"""Gitvc.ipynb

Colaboratory File (used for prototyping):
    https://colab.research.google.com/drive/1MP0cSkbEu9bgC1NkQLKZy1Elgdqmag8c

"""

import pandas as pd
from Training.parsing import get_labels
from Training.create_model import create_model
import Features.feature_extraction as features
import Training.Pre_processing as pre
import ast
from collections import Counter

# To handle Settings Warning
pd.set_option('mode.chained_assignment', None)

# Read uncleaned CSV file
data = pd.read_csv("../Git_logs/data_odoo_2.csv",
                   index_col=False,
                   names=list(
                       "commit id,author,date,comment,changed files,lines added,lines deleted".split(",")))

data.drop(columns=["date"], axis=1, inplace=True)

def remove_merge_commits(data):
    data = data[data["author"] != "Odoo's Mergebot"]
    data[~data['comment'].str.contains('[MERGE]', na=False)]


# print("The shape of data :", data.shape)
# Extract numeric features by using function
# defined in /Features/feature_extraction.py
def extract_num():
    print(">> Extracting numeric values <<\n")
    data['lines added'] = pd.to_numeric(data['lines added'])
    data['lines deleted'] = pd.to_numeric(data['lines deleted'])


    # data['changed files'] = pd.to_numeric(data['changed files'])
    # size_features = features.Size(data)
    # size_features.keep_numeric_data("changed files")
    # size_features.keep_numeric_data("lines deleted")
    # size_features.keep_numeric_data("lines added")


# assigning values to keywords
# Extract keywords and map them to values by
# using function defined in /Features/feature_extraction.py
# assigning values to keywords
def extract_keywords():
    print(">> Extracting keywords from commit <<\n")
    # print(resp)
    commit_msg = features.Key(data)
    resp = commit_msg.map_keywords_to_val("comment")


# assigning values to authors
# Mapping author to experience values
# by using function defined in /Features/feature_extraction.py
def map_authors():
    print(">> Mapping Authors <<\n")
    authors = features.Authors(data, "author")
    resp = authors.map_author_to_val()
    print(resp)


def fill_na():
    print(">> Filling na values <<\n")
    data["changed files"].fillna(0, inplace=True)
    data["lines added"].fillna(0, inplace=True)
    data["lines deleted"].fillna(0, inplace=True)
    data["comment"].fillna("", inplace=True)
    num_of_na = data.isnull().sum()


def misc():
    data.loc[data['changed files'] == " ", 'changed files'] = 0
    data.drop(data[data['changed files'] == 'account: use reply_to header from tmplt""'].index, inplace=True)
    data.loc[data['lines added'] == " 0 insertions(+)", 'lines added'] = 0
    data.loc[data['lines deleted'] == " 0 deletions(-) ", 'lines deleted'] = 0


def label_bugs():
    # Old code
    # buggy_commits = get_labels()
    # with open("./buggy.txt", "w+") as bugs:
    #     bugs.write(buggy_commits)

    # buggy_commits = ['ce39ca8a978b', '6ca06b7027bd', '214a59845f25', 'e8dec0fdf149', '21dd9384d048',
    #                  '56f3f01491f3', '73421c27f01e', 'c0d7a05730dc', '4095c25262dd', '33086d779530', '03afd0f2a1a2', '938ffb92da1e', '0ca97ae3d649', '34e679598be3', '297297696261', '2ded1015d69e', 'dc673bffc207', '6b772af15c31', '8a28cc22fd24', '18e5416636b1', 'eec0b8075655', '506d29371437', '5a25b7dc8774', '15df14b9e186', 'c3e097ff31b8', 'a85023032540', 'a136b4c29a9b', 'ba8a1c7ec24c', 'bae7e32e4bd4', 'b446930dc424', '64e945aa446f', '819056582be7', '5875a253ddd2', '5c7892fe6ba1', 'a64f64aba449', 'c8d7ad9a6bc5', '3b3d35e8b91f', 'cbe2dbb672a6', 'eaa094285e48', '4f40c9da7b26', '3028e9a8649a', '40265731a095', '88a26235ca97', '23a2ae6f4d39', '04ba0e99a44b', 'd33086c03fc1', '218f1c63ea32', '086405344e73', 'b30e280b2d67', '8a399930f316', '955ad1d85d2c', '295b47a4808d', 'cb30f536368c', '91777051d9c1', '1e576ee899d7', 'a74561640400', '748479149772', 'bfbc7c6a184b', 'ff3d1fce1f6c', '8e15a23ca66f', 'e3333d5e074d', 'b6f053b25ef8', 'bc131c0cfb51', '8fc246da31aa', '028768f288ca', 'f52a5a72555d', 'e9be0bb17842', 'c0febb02d8d3', 'd56b35e26e4b', '384647e58326', '72f7139f52a2', '4ecbacaf5957', '685f4eff507e', 'cae1c3977ff2', '5307f47d975c', '4e8ebc7a7248', '55ed70f405a7', '1d23c24d79a0', 'a4cce228cf87', 'a1f003ef35a5', '56d0c1ed9778', 'bdae0a0fe00f', '7e5c7916a2a5', 'bf347e7727b4', '84de7cbcb623', '996b6571b735', '7a691c8eb09b', '7fc655f75e82', '7544c22de9a4', 'bdec8efabf4b', '34c47eecd30b', '950f252ba66c', '32d696ec43a9', '7978d4ba0f09', 'abef1683893c', '9d2cf7325308', '4ddc32313996', 'bdf2711f0166', '92f171dac8f1', '00375756199e', 'a5dccc1586c0', '6fb4ed44a040', '222cca2feb11', '2ab0bd3236c1', '348a44855d65', '8bef7af30706', '928d261c1b8c', 'fffaf735f58f', '3bb3e6a53077', 'c3151daea725', '726653fa7bbc', 'd5b687a48ffb', '67003bd76fdb', '3977e28bafb6', 'f159608e02fa', 'fd09ddb6f3c4', '21e4579551a0', '415525cecceb', '2856d169128b', '7593b887dff4', 'd201a3935714', 'ac76a6b40cac', 'fd86ffd5aa6f', '05546434f051', '4ba4d61903ba', '74c5c00affd9', 'e67b22946d50', '41897f0dbabe', '4b5513cfd47c', '8d5da6e4be05', '40dd12193855', 'ab7ab7ebbb09', 'abc80eff18a5', '2a5488619da2', '2c261a2987f4', 'b9488caa643c', 'ec625a603365', '3fd7b2009ec1', '92cf2474a2b6', '3c32f9b90309', 'abb8328fc40a', '8fbee7978f15', 'c812122d5e12', 'fe6202f34338', 'e8e8d7a956a9', '70eeb2ece959', '020e2a5e8503', 'c8c8eb3d5652', '250e716c3a12', '9219944a5aee', 'c9bed78c2bc6', '296494aaed42', '8b8815f44cc7', '99f4a66de8db', 'd5accc0faea9', 'b17de5f75f68', '93bf26abc1cb', '1be50fdeafcd', '1aa5bc0fdfa4', '369c20a99bd2', 'aa3ce8b594eb', 'cba55c12e469', '4f27e52cabb7', 'd3291207efb5', 'cfe0523714b4', '573e57773b78', 'eb04aa1e395d', '1e6c3bec2c5c', '5ffbcd57ae64', '6e55a3a49666', '536560bbf55d', 'd01787c19d46', '74737865d51b', '78e79073b999', '9690685d652e', 'c61de0cb84b0', '84629a03fa2d', 'd310b3ef578e', '71cd55490ab7', '49aa98ab9970', '3cbdfe880783', 'eeac89f0555b', '4c31a758cf07', '09731b7860ca', 'bbca13541053', '18854caedd54', 'ed26e9eafa31', '345a5a4aa816', '568b258c4359', '66f99636d2d8', '868a77616d2d', 'ab56e637b7f9', '6306441e80a2', '977db823c7c8', '24b57a377fec', '3c9cf1e75302', '9fe9715e9936', '0c8be24ac72c', '4a031781462d', 'd561868bfa40', 'ef0488ef9116', '2b830e5d4116', '8aa8548d8ab6', '8e540558ee16', '6cbe824871da', 'aae1d5782968', 'b252ffb13fc0', '361b711ffc46', '2c6cd3f357f8', '9de1bc0eef6f', 'fd659e908be0', 'eaa93d1bd491', '949381680f2e', 'e20cc70d0824', '2b314aad5c7d', 'f295bdccadec', '7b1e881e60d6', '7b75571fe85f', 'a6f44ee93e44', 'aeed763b0341', 'b026fe7611ad', 'cb339842d4d8', 'efa64513424f', '216cf93b4dab', '2ddc35a5300e', '160a7cf88c9b', '3e2e1d6b905c', '69ccabb212d8', '439fa82676a0', 'a15213c574f6', '898224f11093', 'c25803235a6d', 'b96e633b0b8d', '67c090e48a8b', 'eca99f1f1217', '60f4c40ca564', '2dccf4d6cd07', 'c24a132ee10f', 'e3c7f66e89d7', 'bb281e98f52a', '2a3e4d265737', '5ea27d471e3c', '971ed88798ba', '8734ffb6c2cb', 'df7953f3031a', 'ed34640d3ae7', '841af2acb392', '526f27ddac8b', 'fac1d52e2e69', '0cc8610923d8', '5c4544fb2943', 'a45bb90fac04', 'f1c7a34f0b82', '9efcfbdb9f8d', '0d2be38333d8', 'e80582840ebf', 'c667e95224b8', 'e239934abe45', '6692919d1efc', 'e3a87d351154', '443735949e79', '0fdee29bb477', 'b6193a6b8d56', '4b122ad41d87', '8be6470a826f', 'c1fea08517a6', '50bf8309f88f', '17f5f74af943', '180126755e79', '8970127c036a', '6f247d799a5e', 'b38253f40059', '8f295a64f37e', 'bc79f9248126', '1270eaad6626', '602807acdf20', 'b247aa32529f', 'dbd4114d382c', '1f8b2c5a1bb5', 'b7c746abb8d9', '49bf1bf3d1c3', '8fa9f7d6d4bc', 'dba478332681', '7eab8e26d3d4', '407d9a88a3d2', 'eed8a3468639', '0d6332fdbbea', '9b38bcec1269', 'a3f923f39ea8', '7c123228029e', 'ff6b35f759c6', 'dd3faf40fa7f', '711a48aaa88d', 'dfd01b8c5c7e', '00521bc998a8', '699890d3f0b9', '5f551d235c78', '22c5fc5dd2fc', '7a6269719fb8', '054baf94a68a', '01216345e283', '2c6cd81f30a9', 'd458aca28c25', 'aefb17b12451', 'a97037c6d442', 'fe20747ddcb1', '6a2b4827d4fb', 'e8611b363a10', 'e3f1802d4cfc', 'c37e8c0479ea', 'e3f99885ca78', '16e6907efa55', '27a4c07187c2', '0e4f3bb95991', 'a661b0001555', '65530dfd6a04', '385030338523', '506c9764e0c0', 'f1a85ba70a24', 'ff2efcd1a9b6', '98ee0f766c50', 'd972df33da45', '3ff5fea9339d', '886eca013171', '18e6341dbfad', '5096e724643c', '21ea9d4cc753', 'd2b02cab2983', 'f402afd7b503', '0eee7c68ff42', 'c04065abd8f6', 'caf11fade0e2', 'd43d25020ec4', '3684c8a62ed0', 'cd34f6de727d', '0a540e0ef25a', 'a35df8d37170', 'c8fdf32db130', 'ed2773e38158', '130af96dc155', 'f17e5d33390e', 'fd6946f24abf', 'aaadb232b231', '70e1d5d5bc1a', 'f064437f0671', '2646a34cf08d', 'f205bfcd4ddc', '4eeeb4f172c1', '78565b1dc933', '2a50f359db24', '6b8acd025758', '9e57185449a0', '3ae54b6416a9', '650074e8b2fa', 'e84779749b14', 'fccaa703c492', 'f322816ae826', '3bb666c226e6', '35ccc8bb0694', 'b5a04fd29ff1', '76cf2ae82a45', '73e652818b81', '7fb016f9966b', '654f932b3c9c', '2550c26e29b6', '9d2e82534018', '7d01ed5ee97f', 'f20c3610952d', '9920f20e4c77', '45704b621838', 'd4ac8e7c197a', 'f9a8015ef823', '211dba4a83a1', '3b3279c77e2b', 'b4af54f9c23b', '058cf208a8e7', 'ba2116838ec4', '5d08bdfb0430', '4523a11bed33', 'f27318c8af85', 'eb6c3f62885e', '1dff0b7c4fe5', 'd8b6b35cb3c7', '905e01921f3c', '37ea5dc3160f', '0940bfcfd532', '77e5e8b7ffb7', 'c8dca514e619', 'aa44700dccdc', '284d82623f69', '5999d47d6b53', '36551615b726', 'ff0053b41695', '38d8b0526f0f', '56ee149f113d', 'd8c5cc133580', '1c9a6db16fb4', 'ee1f0ef1ac51', '2b88d71c6e48', '3baac932ca23', 'dc101d12a595', '73505303f881', '02903076c9d7', '5401c15dd7a7', '2f900d4f1ca7', 'eceb17365357', '33b75bb48bcb', '463a214699ac', 'a5e7a4c8ae04', '850e1675eb25', '1fe5145f0cc1', '9a0aaa9e888b', '269aa594111a', '97256fa1fba6', '78c3952c3ebf', '313f69e9487e', 'e10fd34682a0', '604c43640a05', '4da64b3f3c8d', 'ef30f3a6a808', '37c4e24e6956', '4bb31f1d847e', 'a55bc67f0797', '5b563549fa6d', 'ff870099c588', '43745c4cb965', 'bb25b70a749b', '54d1adf31a70', '220f5ae53f66', 'b6288e544614', '0aac1c7cb0c0', '29f02a37f042', '03f95d1803a2', '688e21b6e067', '1345702258ad', 'f9837eb08a31', '1e15d36a23d5', '5f6e94165b49', '6155210d12da', 'cbab786eb2e1', 'c0104303c636', '1c1c0897e8ec', 'c4339e0cec33', 'ce1da231b9c8', '3f495aa4947f', '^5260d22c4d6', 'c058562d7301', '4d0a189796e6']

    # buggy_commits = [bug[:5] for bug in buggy_commits]
    #
    # ins = [0 for _ in range(data.shape[0])]
    # data['buggy'] = ins
    #
    # for i in range(data.shape[0]):
    #     if str(data["commit id"].iloc[i])[:5] in buggy_commits:
    #         data["buggy"].iloc[i]=1

    buggy_commits = ""
    buggy_commits_2 = ""
    with open("../Git_logs/bug_test.txt", "r") as bugs:
        buggy_commits = bugs.read()

    with open("../Git_logs/bug_test_2.txt", "r") as bugs:
        buggy_commits_2 = bugs.read()

    buggy_commits = ast.literal_eval(buggy_commits)
    buggy_commits = [ele.strip() for ele in buggy_commits]

    buggy_commits_2 = ast.literal_eval(buggy_commits_2)
    buggy_commits_2 = [ele.strip() for ele in buggy_commits_2]

    # print(buggy_commits[:5])
    # print(type(buggy_commits[1]))
    # print(buggy_commits[0][0])
    # print("no of buggy file = ", len(buggy_commits))
    buggy_commits.extend(buggy_commits_2)
    print("no of buggy file = ", len(buggy_commits))

    buggy_commits = [bug[:8] for bug in buggy_commits]

    ins = [0 for _ in range(data.shape[0])]
    data['buggy'] = ins
    bugs = 0
    for i in range(data.shape[0]):
        if str(data["commit id"].iloc[i])[:8] in buggy_commits:
            bugs+=1
            data["buggy"].iloc[i] = 1
    print("\n bugs = ", bugs)

    return


def save_dataset():
    data.to_csv("./cleaned_data_latest.csv", index=False)
    print(">> Data saves to ./rf_model_del.csv <<")


remove_merge_commits(data)
extract_keywords()
# map_authors()

data_info = data.info()
num_of_na = data.isnull().sum()

fill_na()
# misc()

data = data.iloc[1:, :]
label_bugs()
data.drop(columns=["commit id"], axis=1, inplace=True)

extract_num()
pre.remove_non_numeric_data(data)
pre.Label_encode(data)
pre.removing_outliers(data)

print(Counter(data["buggy"]))
save_dataset()

print(">>Creating Model<<")
create_model()
