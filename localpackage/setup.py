from pytorch_lightning import LightningModule
import torch.nn as nn
import torch
import numpy as np


class NCF(LightningModule):
    """ Neural Collaborative Filtering (NCF)
    
        Args:
            num_users (int): Number of unique users
            num_items (int): Number of unique items
            ratings (pd.DataFrame): Dataframe containing the movie ratings for training
            all_movieIds (list): List containing all movieIds (train + test)
    """
    
    def __init__(self, num_users, num_items, ratings, all_movieIds):
        super().__init__()
        self.user_embedding = nn.Embedding(num_embeddings=num_users, embedding_dim=8)
        self.item_embedding = nn.Embedding(num_embeddings=num_items, embedding_dim=8)
        self.fc1 = nn.Linear(in_features=16, out_features=64)
        self.fc2 = nn.Linear(in_features=64, out_features=32)
        self.output = nn.Linear(in_features=32, out_features=1)
        self.ratings = ratings
        self.all_movieIds = all_movieIds
        
    def forward(self, user_input, item_input):
        
        # Pass through embedding layers
        user_embedded = self.user_embedding(user_input)
        item_embedded = self.item_embedding(item_input)

        # Concat the two embedding layers
        vector = torch.cat([user_embedded, item_embedded], dim=-1)

        # Pass through dense layer
        vector = nn.ReLU()(self.fc1(vector))
        vector = nn.ReLU()(self.fc2(vector))

        # Output layer
        pred = nn.Sigmoid()(self.output(vector))

        return pred
    
    def training_step(self, batch, batch_idx):
        user_input, item_input, labels = batch
        predicted_labels = self(user_input, item_input)
        loss = nn.BCELoss()(predicted_labels, labels.view(-1, 1).float())
        return loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters())

    def train_dataloader(self):
        return DataLoader(MovieLensTrainDataset(self.ratings, self.all_movieIds),
                          batch_size=512, num_workers=4)


def getUserRecommendationsShort(usersMovies,model,users, moviePool, links, movieTitles ):
  # reformat data in order to be understood by model
  userMoviesInts = [int(movieId[2:]) for movieId in usersMovies]
  UserModelCompatibleMovies = [(links[links['imdbId']==movieId]['movieId'].values[0]) for movieId in userMoviesInts if links['imdbId'].isin([movieId]).sum()]


  reccommendableMoviePool = list(set(moviePool) - set(UserModelCompatibleMovies))

  if len(UserModelCompatibleMovies)>0:
    bestUser =0

    for user in users:
      predicted_labels = np.squeeze(model(torch.tensor([user]*len(UserModelCompatibleMovies)), torch.tensor(UserModelCompatibleMovies)).detach().numpy())
      userSimilarityScore = np.sum(predicted_labels)
      if userSimilarityScore>bestUser:
        bestUser = user
      break
    print(bestUser)
    bestMovies = np.squeeze(model(torch.tensor([bestUser]*len(reccommendableMoviePool)), torch.tensor(reccommendableMoviePool)).detach().numpy())
    
    titles = [movieTitles[movieTitles['movieId']==movie]['title'].values[0]for movie in np.argsort(bestMovies)[::-1][0:10].tolist() ]
    print(titles)
    top10_items = ["tt"+"0"*(7-len(str(links[links['movieId']==reccommendableMoviePool[i]]['imdbId'].values[0])))+str(links[links['movieId']==reccommendableMoviePool[i]]['imdbId'].values[0]) for i in np.argsort(bestMovies)[::-1][0:10].tolist()]
    return top10_items
  return "tt0000000"