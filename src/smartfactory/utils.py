import cv2
import os
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder
from django_pandas.io import read_frame
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors
"""
utils file, contains code which are generic
"""
from django.core.management import call_command

def is_image_aspect_ratio_valid(img_url):
    img = cv2.imread(img_url)
    dimensions = tuple(img.shape[1::-1]) # gives: (width, height)
    # print("dimensions: " + str(dimensions))
    aspect_ratio = dimensions[0] / dimensions[1] # divide w / h
    # print("aspect_ratio: " + str(aspect_ratio))
    if aspect_ratio < 1:
        return False
    return True


def is_image_size_valid(img_url, mb_limit):
    image_size = os.path.getsize(img_url)
    # print("image size: " + str(image_size))
    if image_size > mb_limit:
        return False
    return True


def encoding_data(recommendations, recommendation):
    df_ = read_frame(recommendations)
    df_search = read_frame(recommendation)
    # ----- main filteration of the data for furture use
    df_['sku'] = df_['Sku'].astype(str).str[:-2].astype(np.str)
    df_search['sku'] = df_search['Sku'].astype(str).str[:-2].astype(np.str)

    df_['zlqty'] = df_.groupby('sku')['ZlQty'].transform('sum')
    df_ = df_.drop_duplicates(subset='sku', keep="last")

    df_['Categories'] = df_['Categories'].str.replace('\W', '')
    df_ = df_[['sku', 'StatusCode', 'SaisonRetourenCode', 'GeschlechtCode', 'RayonCode', 'WarenArtCode', 'WUCode', 'WACode', 'AlterCode', 'Farbe', 'Material', 'Eti', 'VP', 'zlqty', 'SoldOneYear', 'ShortDescription', 'Categories']]
    df_search = df_search[['StatusCode', 'SaisonRetourenCode', 'GeschlechtCode', 'RayonCode', 'WarenArtCode', 'WUCode', 'WACode', 'AlterCode', 'Farbe', 'Material', 'Eti', 'VP', 'SoldOneYear', 'ShortDescription', 'Categories']]
    df_search['Categories'] = df_search['Categories'].str.replace('\W', '')

    popularity_threshold = 3
    df_ = df_.query('zlqty >= @popularity_threshold')
    df_['Farbe'] = df_['Farbe'].fillna('null')
    df_['Material'] = df_['Material'].fillna('null')
    df_['ShortDescription'] = df_['ShortDescription'].fillna('null')
    df_['Categories'] = df_['Categories'].fillna('null')
    df_['StatusCode'] = df_['StatusCode'].fillna('null')

    df = df_[['StatusCode', 'SaisonRetourenCode', 'GeschlechtCode', 'RayonCode', 'WarenArtCode', 'WUCode','WACode', 'AlterCode', 'Farbe', 'Material', 'Eti', 'VP', 'zlqty', 'SoldOneYear', 'ShortDescription','Categories']]

    df.to_csv('/Users/zahid/Downloads/file3.csv', header=True, index=True)


    df_object_columns = df.iloc[:, :].select_dtypes(include=['object']).columns
    print(df_object_columns)
    return "ddd"
    df_char = pd.DataFrame(df, columns=['Farbe', 'Material', 'ShortDescription', 'Categories', 'StatusCode'])
    df_search_char = pd.DataFrame(df_search, columns=['Farbe', 'Material', 'ShortDescription', 'Categories','StatusCode'])

    # instantiate `MultiColumnLabelEncoder`
    mcle = MultiColumnLabelEncoder(columns=df_object_columns)
    mcle.fit(df_char)
    df_char = mcle.transform(df_char)
    df_char = pd.DataFrame(df_char,columns=['Farbe', 'Material', 'ShortDescription', 'Categories', 'StatusCode'])

    df_search_char = mcle.transform(df_search_char)
    df_search_char = pd.DataFrame(df_search_char,columns=['Farbe', 'Material', 'ShortDescription', 'Categories', 'StatusCode'])

    df[['Farbe', 'Material', 'ShortDescription', 'Categories', 'StatusCode']] = df_char[['Farbe', 'Material', 'ShortDescription', 'Categories', 'StatusCode']].to_numpy()
    del df['zlqty']

    df_search[['Farbe', 'Material', 'ShortDescription', 'Categories', 'StatusCode']] = df_search_char[['Farbe', 'Material', 'ShortDescription', 'Categories', 'StatusCode']].to_numpy()

  #  return "sdfs"
    scaling = MinMaxScaler()
    scaling.fit(df)
    df_scaled = scaling.transform(df)

    df_search = scaling.transform(df_search)
    #np.savetxt("/Users/zahid/Downloads/file4.csv", orignal, delimiter=",")


  #  df_search = scaling.fit_transform(df_search)

    #print(df_scaled)
    #print(df_search)
    #return "vff"
   # df_scaled.to_csv('/Users/zahid/Downloads/file3.csv', header=True, index=True)
   # df_search.to_csv('/Users/zahid/Downloads/file4.csv', header=True, index=True)
   # return "sdf"

    df_scaled = pd.DataFrame(df_scaled, columns=['StatusCode', 'SaisonRetourenCode', 'GeschlechtCode', 'RayonCode', 'WarenArtCode', 'WUCode', 'WACode', 'AlterCode', 'Farbe', 'Material', 'Eti', 'VP', 'SoldOneYear', 'ShortDescription', 'Categories'])
    df_search_scaled = pd.DataFrame(df_search, columns=[ 'StatusCode', 'SaisonRetourenCode', 'GeschlechtCode', 'RayonCode', 'WarenArtCode', 'WUCode', 'WACode', 'AlterCode', 'Farbe', 'Material', 'Eti', 'VP', 'SoldOneYear', 'ShortDescription', 'Categories'])
    #print(df_search_scaled.iloc[0,:].values.reshape(1, -1))
   # df_scaled.to_csv('/Users/zahid/Downloads/file4.csv', header=True, index=True)
   # df.to_csv('/Users/zahid/Downloads/file2.csv', header=True, index=True)

    model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
    model_knn.fit(df)
    distances, indices = model_knn.kneighbors(df_search.iloc[0,:].values.reshape(1, -1), n_neighbors=5)
    for i in range(0, len(distances.flatten())):
        print('{0}: {1}, with distance of {2}:'.format(i, df_.iloc[df_.index[indices.flatten()[i]],:].values.reshape(1, -1),distances.flatten()[i]))

    for i in range(0, len(distances.flatten())):
        print('{0}: {1}, with distance of {2}:'.format(i, df.index[indices.flatten()[i]],distances.flatten()[i]))

    return "ffff"

    query_index = np.random.choice(df_scaled.shape[0])
    df_scaled.iloc[query_index, :].values.reshape(1, -1)
    return df_search

    df_orignal = scaling.inverse_transform(df_scaled)
    df_orignal = pd.DataFrame(df_orignal, columns=['StatusCode', 'SaisonRetourenCode', 'GeschlechtCode', 'RayonCode', 'WarenArtCode', 'WUCode', 'WACode', 'AlterCode', 'Farbe', 'Material', 'Eti', 'VP', 'ZlQty', 'SoldOneYear', 'ShortDescription', 'Categories'])

    df_orignal_four_column = df_orignal[['Size', 'Farbe', 'Material', 'ShortDescription']]
    cols = ['size', 'farbe', 'material', 'short_description']
    df_int = df_orignal[cols].applymap(np.int64)
    df_orignal_four_column = mcle.inverse_transform(df_int)
    df_orignal_four_column = pd.DataFrame(df_orignal_four_column, columns=['Size', 'Farbe', 'Material', 'ShortDescription'])
    df = df.assign(Size=df_orignal_four_column['Size'])
    df = df.assign(Farbe=df_orignal_four_column['Farbe'])
    df = df.assign(Material=df_orignal_four_column['Material'])
    df = df.assign(ShortDescription=df_orignal_four_column['ShortDescription'])

    return data

    df_char.to_csv('/Users/zahid/Downloads/file2.csv', header=True, index=True)
    return data
    df_char = pd.DataFrame(df_char, columns=['size', 'farbe', 'material', 'short_description'])

    print(df_char)
    return data

    #df_text_columns.to_csv('/Users/zahid/Downloads/file2.csv', header=True, index=True)

    scaled_df = pd.DataFrame(scaled_df, columns=['size', 'farbe', 'material', 'short_description'])

    np.savetxt("/Users/zahid/Downloads/file2.csv", scaled_df, delimiter=",")

    #df = pd.DataFrame(df, columns=['size', 'farbe', 'material', 'short_description'])

    return data

class MultiColumnLabelEncoder(LabelEncoder):
    """
    Wraps sklearn LabelEncoder functionality for use on multiple columns of a
    pandas dataframe.

    """
    def __init__(self, columns=None):
        self.columns = columns

    def fit(self, dframe):
        """
        Fit label encoder to pandas columns.

        Access individual column classes via indexig `self.all_classes_`

        Access individual column encoders via indexing
        `self.all_encoders_`
        """
        # if columns are provided, iterate through and get `classes_`
        if self.columns is not None:
            # ndarray to hold LabelEncoder().classes_ for each
            # column; should match the shape of specified `columns`
            self.all_classes_ = np.ndarray(shape=self.columns.shape,
                                           dtype=object)
            self.all_encoders_ = np.ndarray(shape=self.columns.shape,
                                            dtype=object)
            for idx, column in enumerate(self.columns):
                # fit LabelEncoder to get `classes_` for the column
                le = LabelEncoder()
                le.fit(dframe.loc[:, column].values)
                # append the `classes_` to our ndarray container
                self.all_classes_[idx] = (column,
                                          np.array(le.classes_.tolist(),
                                                  dtype=object))
                # append this column's encoder
                self.all_encoders_[idx] = le
        else:
            # no columns specified; assume all are to be encoded
            self.columns = dframe.iloc[:, :].columns
            self.all_classes_ = np.ndarray(shape=self.columns.shape,
                                           dtype=object)
            for idx, column in enumerate(self.columns):
                le = LabelEncoder()
                le.fit(dframe.loc[:, column].values)
                self.all_classes_[idx] = (column,
                                          np.array(le.classes_.tolist(),
                                                  dtype=object))
                self.all_encoders_[idx] = le
        return self

    def fit_transform(self, dframe):
        """
        Fit label encoder and return encoded labels.

        Access individual column classes via indexing
        `self.all_classes_`

        Access individual column encoders via indexing
        `self.all_encoders_`

        Access individual column encoded labels via indexing
        `self.all_labels_`
        """
        # if columns are provided, iterate through and get `classes_`
        if self.columns is not None:
            # ndarray to hold LabelEncoder().classes_ for each
            # column; should match the shape of specified `columns`
            self.all_classes_ = np.ndarray(shape=self.columns.shape,
                                           dtype=object)
            self.all_encoders_ = np.ndarray(shape=self.columns.shape,
                                            dtype=object)
            self.all_labels_ = np.ndarray(shape=self.columns.shape,
                                          dtype=object)
            for idx, column in enumerate(self.columns):
                # instantiate LabelEncoder
                le = LabelEncoder()
                # fit and transform labels in the column
                dframe.loc[:, column] =\
                    le.fit_transform(dframe.loc[:, column].values)
                # append the `classes_` to our ndarray container
                self.all_classes_[idx] = (column,
                                          np.array(le.classes_.tolist(),
                                                  dtype=object))
                self.all_encoders_[idx] = le
                self.all_labels_[idx] = le
        else:
            # no columns specified; assume all are to be encoded
            self.columns = dframe.iloc[:, :].columns
            self.all_classes_ = np.ndarray(shape=self.columns.shape,
                                           dtype=object)
            for idx, column in enumerate(self.columns):
                le = LabelEncoder()
                dframe.loc[:, column] = le.fit_transform(
                        dframe.loc[:, column].values)
                self.all_classes_[idx] = (column,
                                          np.array(le.classes_.tolist(),
                                                  dtype=object))
                self.all_encoders_[idx] = le
        return dframe.loc[:, self.columns].values

    def transform(self, dframe):
        """
        Transform labels to normalized encoding.
        """
        if self.columns is not None:
            for idx, column in enumerate(self.columns):
                dframe.loc[:, column] = self.all_encoders_[
                    idx].transform(dframe.loc[:, column].values)
        else:
            self.columns = dframe.iloc[:, :].columns
            for idx, column in enumerate(self.columns):
                dframe.loc[:, column] = self.all_encoders_[idx]\
                    .transform(dframe.loc[:, column].values)
        return dframe.loc[:, self.columns].values

    def inverse_transform(self, dframe):
        """
        Transform labels back to original encoding.
        """
        if self.columns is not None:
            for idx, column in enumerate(self.columns):
                dframe.loc[:, column] = self.all_encoders_[idx]\
                    .inverse_transform(dframe.loc[:, column].values)
        else:
            self.columns = dframe.iloc[:, :].columns
            for idx, column in enumerate(self.columns):
                dframe.loc[:, column] = self.all_encoders_[idx]\
                    .inverse_transform(dframe.loc[:, column].values)
        return dframe.loc[:, self.columns].values


def categories(df):

    for index,i in zip(df.index,df['categories']):
        list1 = []
        for j in range(len(i)):
            list1.append((i[j]['categoryRoots'][len(i[j]['categoryRoots'])-1]['name']))
        df.loc[index,'categories_'] = str(list1)

    df['categories_'] = df['categories_'].str.strip('[ ]').str.replace(' ', '').str.replace("'", '')
    df['categories_'] = df['categories_'].str.split(',')


    for i, j in zip(df['categories_'], df.index):
        list2 = []
        list2 = i
        list2.sort()
        df.loc[j, 'categories_'] = str(list2)
    df['categories_'] = df['categories_'].str.strip('[]').str.replace(' ', '').str.replace("'", '')
    df['categories_'] = df['categories_'].str.split(',')

    category_list = []
    category_list2 = []
    for index, row in df.iterrows():
        categories = row["categories_"]
        for category in categories:
            if category not in category_list:
                category_list.append(category)
    for n in category_list:
        category_list2.append({"category":n})
    return category_list2


def is_empty_or_null(value):
    if (not value) or (value == '') or (value is None) or (value == 'null'):
        return True
    return False


# run elastic search command to rebuild index
def rebuild_elasticsearch_index():
    call_command('search_index', '--rebuild', '-f')


# run elastic search command to delete index
def delete_elasticsearch_index():
    call_command('search_index', '--delete', '-f')

