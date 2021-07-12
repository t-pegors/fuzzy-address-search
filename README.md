This browser-styled tool takes a dataset as input and outputs search results based on a TF-IDF search algorithm.
<hr>
<img src="/webtool/static/screenshots/step_1.png" alt="step_1" width="500"/>
Step 1: Upload a csv with the data you want to search. There should be a single column of interest to search. If columns need to be merged or edited, do this before uploading the data.
<hr>
<img src="/webtool/static/screenshots/step_2.png" alt="step_2" width="500"/>
Step 2: Here, pick the column you want to search. The other columns will be returned as part of the search output. This process of vectorizing the data in the selected column can take quite awhile depending on the size of the dataset. For example, I tested a dataset of 3.5 million rows, and the vectorization process took approximately 3 and a half minutes.
<hr>
<img src="/webtool/static/screenshots/step_3.png" alt="step_3" width="500"/>
Step 3: You can enter more than one search address into the box. The output contains an additional column with the search address.
<hr>
<img src="/webtool/static/screenshots/step_4.png" alt="step_4" width="500"/>
Step 4: Set your "match" threshold. The similarity score will be output as an additional column, so it is recommended to set this threshold lower than needed - filtering can take place on the returned dataset.
<hr>
<img src="/webtool/static/screenshots/step_5.png" alt="step_5" width="500"/>
Step 5: Search your data. All dataset columns will be returned along with 2 additional columns: search term and similarity score. These results can be output to a CSV file.
