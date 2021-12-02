# TURF
Horse races predictive model

![Results](https://github.com/clementpiat/TURF/blob/master/visualisations/simulation_modele_basique2.png)

## Training a model

Train a model (sklearn classifier and pytorch network) that predicts if a horse is going to finish in the first positions.
```
python train_place.py
```
Edit the variables directly in the script.
```
date = "2015-01-01_2017-01-01"
specialite = "PLAT"
needed_columns = ["ordreArrivee"]
```

## Evaluate the model performance on an unseen time range

```
python simulate.py
```
Edit the variables directly in the script.
```
date = "2015-01-01_2015-01-03"
model_folder = "09_11_2020-16h16m00s"
```
