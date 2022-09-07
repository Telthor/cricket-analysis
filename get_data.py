import kaggle
import numpy

# Download the data

kaggle.api.authenticate()

kaggle.api.dataset_download_files('cclayford/cricinfo-statsguru-data', path='data', unzip=True)