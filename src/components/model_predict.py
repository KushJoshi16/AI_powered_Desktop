from src.components.data_ingestion import DataIngestionConfig, DataIngestion
from sklearn.metrics import silhouette_samples,silhouette_score
from src.utils import scale
from sklearn.cluster import KMeans

class Model:

    def __init__(self) -> None:
        self.data = DataIngestion()
    
    def get_silhouette_avg(self,X,range_n_clusters):
        """
        Calculates performance of clusters as per silhouette score among different n_cluster values and returns the best labels
        """
        ms = -1
        cc = range_n_clusters[0]
        y_kmeans = None
        for n_clusters in range_n_clusters:
            try:
                clusterer = KMeans(n_clusters=n_clusters,init = 'k-means++', random_state=10)
                cluster_labels = clusterer.fit_predict(X)

                # The silhouette_score gives the average value for all the samples.
                # This gives a perspective into the density and separation of the formed
                # clusters
    #             sample_silhouette_values = silhouette_samples(X, cluster_labels)

                silhouette_avg = silhouette_score(X, cluster_labels)
                print("For n_clusters =", n_clusters,
                    "The average silhouette_score is :", silhouette_avg)
                ms = max(ms,silhouette_avg)
                cc = max(cc,n_clusters)
                y_kmeans = cluster_labels

                # Compute the silhouette scores for each sample
            except Exception as e:
                continue
            return ms,cc,y_kmeans




    def fit_predict(self):
        """
        Finds the best scalar function and then returns the dataframe with labels in form of a dictionary
        """
        df = self.data.initiate_data_ingestion()
        X = df.iloc[:,[-2,-1]]
        formula_list = ['polynomial','log','exp1','default']
        ssf = -1
        MSF = formula_list[-1]
        cc = 2
        y_kmeans = None
        for formula in formula_list:
            try:
                X['utility'] = X.apply(lambda x: scale(x.click, x.del_T,'exp1'), axis=1)
                print(f"For {formula} formula:")
                score,cc,cl = self.get_silhouette_avg(X,range_n_clusters=[1,2,3])
                if score > ssf:
                    ssf = score
                    # MSF = formula
                    # n_c = cc
                    y_kmeans = cl
                    df['utility'] = X['utility']
            except Exception as e:
                pass
        df['labels'] = y_kmeans
        r_dic = { val[0]: [val[1],val[2],val[3],val[4]] for val in df.values}
        return r_dic


        
 
if __name__ == "__main__":
    kmeans = Model()
    y_kmeans = kmeans.fit_predict()
    print(y_kmeans)



    