# Branch-Trace-Analysis

### Abstract

Branch prediction is a technique used in computer architecture schemes to reduce the overhead cost of branch operations. The present paper examines the application of the following static and dynamic branch prediction methods presented in Santa Clara University’s Advanced Computer Architecture (COEN 313) course: Always Taken, Always Not Taken, N-Bit, Correlating, and Gshare. The Prophet-Critic hybrid predictor is also implemented as a potential method of custom hybrid branch prediction by the authors. Analysis of the aforementioned methods was compared based on the resulting misprediction rates observed upon application to large datasets. Empirical results concluded a substantial performance improvement using dynamic and custom branch prediction techniques over static methods, yielding hit rates of up to 90%. The substantial improvements in performance can be attributed to the active analysis of the branch pattern behaviors. Together, these findings recommend that dynamic techniques of branch prediction are used to improve instruction pipelining and increase CPU efficiency.

Keywords: computer architecture, branch prediction, static, dynamic, hybrid, misprediction rate

### 1 Introduction

This paper evaluates various branch prediction techniques by analyzing branch log files using higher-level languages like python or C. These various techniques are then compared against one another by using their misprediction rates as the main metric. First, the paper will discuss the background surrounding branch prediction and the techniques we used. It’ll then transition into the experiment section where the setup, design, and results of each algorithm will be discussed. These results will then be compared directly with the custom branch predictor used and possible improvements in the overall experiment will be discussed. The paper will then wrap up with some key takeaways and concluding remarks drawn out from the experiment.

### 2 Motivation

Throughout the COEN 313 class, we have talked about branch prediction algorithms and techniques that can be used to reduce clock cycles and therefore increase performance. In this project, our goal was to test the effectiveness of such prediction algorithms on various branch trace log files. These techniques include the static prediction of only guessing branch taken/not taken, dynamic prediction through the use of n-bit prediction, advanced dynamic prediction through Gshare and correlating prediction, and another form of advanced branch prediction known as a Prophet-Critic hybrid prediction model which can use two of the previously listed techniques together [1]. The main metric used to measure the effectiveness of an algorithm was the misprediction rate where the lower the misprediction rate, the better the algorithm can predict branches.

### **3 Experiments**

##### 3.1 Setup

Each algorithm was simulated using Python, and the custom branch predictor our team chose was the Prophet-Critic hybrid prediction model with Gshare as the prophet and a 3-bit predictor as the critic [1]. The four main log files contained over 69.4 million lines total and each file came from a different context of operation. This ensures that the algorithms differ in relative performance from file to file. All the prediction scripts were executed through the terminal where the output was the misprediction rate for each file. Below are the general statistics on all the branch trace files:

| **Filename** | **art.br.txt** | **mcf.br.txt** | **sjeng.br.txt** | **sphinx3.br.txt** |
| ------------------ | -------------------- | -------------------- | ---------------------- | ------------------------ |
| # Branches         | 15,061,011           | 19,518,883           | 17,102,954             | 17,826,992               |
| Taken              | 11,048,300           | 10,925,542           | 11,249,775             | 9,395,761                |
| Not Taken          | 4,012,711            | 8,593,341            | 5,853,179              | 8,431,231                |
| Taken %            | 73.36%               | 55.97%               | 65.78%                 | 52.71%                   |
| Not Taken          | 26.64%               | 44.03%               | 34.22%                 | 47.29%                   |
| Distinct           | 55                   | 76                   | 1235                   | 438                      |

Table 3.1: General Trace Analysis

##### 3.2 Results

Listed below are the results our group found for each branch prediction algorithm: a graph showing the results side by side can be found labeled Figure 7.1:Bar Graph of branch prediction algorithm vs misprediction rate for each log file in the appendices.

| Filename                   | art.br.txt | mcf.br.txt | sjeng.br.txt | sphinx3.br.txt |
| -------------------------- | ---------- | ---------- | ------------ | -------------- |
| # branches predicted taken | 15,061,011 | 19,518,883 | 17,102,954   | 17,826,992     |
| Actual # taken             | 11,048,300 | 10,925,542 | 11,249,775   | 9,395,761      |
| Taken Misprediction Rate   | 0.266      | 0.44       | 0.342        | 0.473          |

Table 3.2: Static Branch Always Taken


| Filename                       | art.br.txt | mcf.br.txt | sjeng.br.txt | sphinx3.br.txt |
| ------------------------------ | ---------- | ---------- | ------------ | -------------- |
| # branches predicted not taken | 15,061,011 | 19,518,883 | 17,102,954   | 17,826,992     |
| Actual # taken                 | 4,012,711  | 8,593,341  | 5,853,179    | 8,431,231      |
| Taken Misprediction Rat        | 0.734      | 0.56       | 0.658        | 0.527          |

Table 3.3: Static Branch Always Not Taken


| Filename | art.br.txt | mcf.br.txt | sjeng.br.txt | sphinx3.br.txt |
| -------- | ---------- | ---------- | ------------ | -------------- |
| 1 Bit    | 0.107      | 0.203      | 0.169        | 0.107          |
| 2 Bit    | 0.056      | 0.162      | 0.133        | 0.061          |
| 3 Bit    | 0.056      | 0.159      | 0.131        | 0.06           |

Table 3.4: Dynamic Branch Predictor


| Filename    | art.br.txt | mcf.br.txt | sjeng.br.txt | sphinx3.br.txt |
| ----------- | ---------- | ---------- | ------------ | -------------- |
| Correlating | 0.054      | 0.16       | 0.193        | 0.124          |
| Gshare      | 0.054      | 0.176      | 0.246        | 0.135          |

Table 3.5: Advanced Dynamic Branch Predictor


| Filename       | art.br.txt | mcf.br.txt | sjeng.br.txt | sphinx3.br.txt |
| -------------- | ---------- | ---------- | ------------ | -------------- |
| Prophet-Critic | 0.512      | 0.384      | 0.397        | 0.406          |

Table 3.6: Custom Branch Predictor/Prophet-Critic Branch Predictor


##### 3.3 Design and Rationale

We chose to implement the Prophet-Critic hybrid as our custom branch predictor. Prophet-Critic utilizes two different branch predictors, labeled “prophet” and “critic” respectively, to make a final branch prediction. The prophet (using Gshare implementation) will make predictions 4 branches into the future, operating under the assumption that its predictions are correct to make new predictions which we will label the “branch future.” The critic (which uses 3-bit predictor logic) then uses the complete branch history and the branching future provided by the prophet as aggregate data in order to make a prediction and produces a result that will either “agree” or “disagree” with the prophet. The critic’s prediction will be the Prophet-Critic’s final prediction for each branch, with the reasoning that it can make more accurate predictions given the additional information on the branch behavior [1]. However, the prophet will be responsible for accurately predicting the majority of branches with the critic acting primarily as a fail-safe to correct any mispredictions.

### 4 Analysis

When examining the results, our team decided to treat the straightforward take or do not take branch prediction algorithms as baselines: this is because of how simple the decision making is for both algorithms as both either takes the branch or does not take the branch in all cases. For comparing the results, we looked at the average of the difference in misprediction rate between both baselines and each of the branch prediction algorithms to obtain the percentage decrease in misprediction rate as seen in Figure 4.1: this comparison shows how well each branch prediction algorithm does compare to the average baseline.  In every case, each branch prediction algorithm outperformed the average baseline by at least 16%, and for the overall best case, the Correlating, Gshare, and Prophet-Critic all outperformed the baseline by 44.6%.

1. **Percent Decrease Misprediction Rate =  [(MPT - MPA) +  (MPD - MPA) ] ፥ 2where  MPT is the misprediction rate for Always Take, MPD is the misprediction rate for Always Don’t Take, and MPA is the misprediction rate for the algorithm being looked at.**


<img src="https://github.com/jayteaftw/Branch-Trace-Analysis/blob/main/images/image1.png" height="700" />

However in a real-world scenario it is unlikely one is unable to choose which branch prediction algorithm should be used for each individual program: it is important then to contextualize the results by taking the average of each percentage decrease in misprediction rate as seen in Figure 4.2. Overall, each branch prediction algorithm had similar average performances with the 3-bit predictor performing the best and the 1-bit predictor performing the worst. Noticeably, the Prophet-Critic algorithm outperformed the Gshare algorithm which is reasonable since in our case the Gshare is the prophet while the 3-bit Predictor is the critic. Improvements could possibly be achieved by swapping both algorithms’ roles since individually the 3-bit Predictor outperformed the Gshare.



<img src="https://github.com/jayteaftw/Branch-Trace-Analysis/blob/main/images/image2.png" height="500" />

### 5 Conclusion

After carrying out the experiments outlined above, the benefits of branch prediction are evident. The implementation of various techniques can influence the performance of branch predictors drastically, improving the accuracy of prediction up to 46% compared to the baselines based on our experimental results. By predicting in advance whether a branch is taken or not, CPUs can improve computational performance accordingly through better pipelining instructions in any given clock cycle. Reducing the overhead induced by mispredicted branches through the use of advanced branch prediction techniques similar to those outlined in this paper is critical to the continued improvement of modern-day processor efficiency.


### 6 References

[1] Mittal, Sparsh. “A Survey of Techniques for Dynamic Branch Prediction.” ArXiv.org, 1 Apr. 2018, https://arxiv.org/abs/1804.00261. 


### 7 Appendices


<img src="https://github.com/jayteaftw/Branch-Trace-Analysis/blob/main/images/image3.png" height="1000" />

**Figure 7.1: Bar Graph of branch prediction algorithm vs misprediction rate for each log file**
