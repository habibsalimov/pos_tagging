# 🔤 Modern Turkish POS Tagger

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)](https://pytorch.org)
[![Transformers](https://img.shields.io/badge/🤗-Transformers-yellow.svg)](https://huggingface.co/transformers)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A **modern, high-performance** Part-of-Speech (POS) tagger for Turkish language, featuring both traditional and state-of-the-art transformer-based approaches. This project modernizes the original Brill tagger implementation with cutting-edge NLP technologies.

## 🌟 Features

### 🚀 **Multiple Model Support**
- **🧠 BERTurk**: State-of-the-art Turkish BERT model
- **⚡ DistilBERT**: Lightweight multilingual model  
- **📚 Legacy Brill**: Original rule-based tagger (backward compatibility)

### 🎯 **Modern Architecture**
- **Python 3.9+** compatibility
- **Type hints** and modern code practices
- **Modular design** with clean separation of concerns
- **Comprehensive error handling** and logging

### 🌐 **Web Interface & API**
- **Beautiful web interface** with real-time tagging
- **RESTful API** endpoints
- **Batch processing** support
- **Docker containerization**

### 📊 **Advanced Analytics**
- **Performance benchmarking** tools
- **Comparative analysis** between models
- **Detailed evaluation metrics**
- **Visualization dashboards**

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/turkish-pos-tagger.git
cd turkish-pos-tagger

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
from modern_pos_tagger import ModernTurkishPOSTagger

# Initialize with different models
tagger = ModernTurkishPOSTagger(model_type="berturk")  # or "legacy", "distilbert"

# Tag a sentence
result = tagger.tag("Bunu başından beri biliyordum zaten .")
print(result)
# Output: [('Bunu', 'Pron'), ('başından', 'Noun'), ('beri', 'Postp'), ...]
```

### Web Interface

```bash
# Start the web service
python web_service.py

# Open your browser to http://localhost:8000
```

![Web Interface Demo](img/web_interface_demo.png)

## 🐳 Docker Support

### Quick Run
```bash
# Build and run with Docker
docker build -t modern-turkish-tagger .
docker run -p 8000:8000 modern-turkish-tagger
```

### Development
```bash
# Run with volume mounting for development
docker run -v $(pwd):/app -p 8000:8000 modern-turkish-tagger
```

### Implementation Idea

* In this part-of-speech tagger application, a transformation based POS system is implemented. In this approach, transformation-based tagger uses rules to specify which tags are possible for words and supervised learning to examine possible transformations, improvements and re-tagging.
* Using NLTK functions, tagged corpus provided in [development.sdx](development.sdx) is read for training and validation purposes. Then, this set is randomly divided into training and development with 85% and 15%.
* As a transformation-based tagger, Brill tagger of NLTK is implemented with maximum rules of 300 and minimum score of 3. Brill tagger uses a general tagging method at the first stage and a trigram tagger is used for that purpose. Back-off stages of this trigram tagger is provided in the next page. Since sufficient information cannot be found about rule templates of Brill tagger, default templates given in [demo code](http://nltk.googlecode.com/svn/trunk/doc/api/nltk.tag.brill-pysrc.html) is directly used.
* Considering k-fold cross validation, this tagger is trained and its performance is tracked, which will be explained in the next section. Flow of operations is shown as a diagram in the following page.
![](img/flow.png)

### Results
* The accuracy of this method is tracked for each folding stage in order to avoid over fitting. Since this tagger will be used for tagging unseen sentences we should avoid generating a model which over fits to our development set.
* For 10-fold validation, accuracy of the model can be plotted as below:
![](img/accuraccy-results.png)
* Considering the plot above, the tagger is evaluated at most 6 times by folding training and evaluation tests. The final tagger provided is expected to have 95% of accuracy on development as can be seen from the figure. This final tagger is saved to [my_tagger.yaml](my_tagger.yaml) file by [training_tagger](training_tagger.py) module and it is exported when [pos_tagger](pos_tagger.py) module is called.

### Future Work
* The main problems related to this model can be listed as following:
  * Considering the relatively small development set, there is a high probability of over fitting. Therefore, accuracy level of this model in unseen data can vary very largely.
  * Although implemented, good source of information about Brill rule templates cannot be found. Therefore, better rule templates can be found or unnecessary ones can be eliminated.
  * Considering Turkish as an agglutinative language, rule based methods can be used as back-off or base stage of Brill tagger. Because adding another affix can mislead the tagger as following:

| Function Call      	| Tags                                                        	|
|--------------------	|-------------------------------------------------------------	|
| tag('Ali koş !')   	| [('Ali', 'Noun_Nom'), ('koş’, 'Verb'), ('!', 'Punc')]       	|
| tag('Ali koştu .') 	| [('Ali', 'Noun_Nom'), ('koştu', 'Noun_Nom'), ('.', 'Punc')] 	|

### Conclusion
* To conclude, when the model is evaluated with random parts from development set, accuracy level is calculated as following:

| # of Trial 	| Minimum 	| Maximum 	| Average 	| Std. Dev. 	|
|:------:	|:-------:	|:-------:	|:-------:	|:---------:	|
|   49   	|   91%   	|   96%   	|   95%   	|     1%    	|

* As it is mentioned in Results part, this level of accuracy was expected on random parts of development set. Considering mentioned possible improvements, this model can be enhanced to result with a higher accuracy, especially on tagging unseen sentences.
