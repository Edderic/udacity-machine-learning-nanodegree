
TODO:

- What happens if it gets a new timezone that was not well-represented earlier?
  - What if the distribution is just like the general distribution consisting
    of all timezones? See next month and next next month
  - What if... is just random? See next month and next next month
  - What if it is heavily focused at one section? (9 PM)

    - How much err
  -
  - and lots of it?
  - Compare how each model does to seeing new data.
  - What happens if the same thing again happens for the subsequent month?
    - Does error go down by a lot?
    - Which error


Metric should not take into account six

- Ex

- How does knowing about timezone affect model performance?
  - Perform ANOVA to determine whether or not one of the groups is really
    different from the others

- What happens when you perturb the input?
  - Find the month that it did the worst. Use that sample to generate new data.
    See how it performs.

- What happens if we run the optimizer for a 1000 iterations?
  -
How does your model compare against the Ruby benchmark

- Calculate analysis of variance for timezones

- How does the model perform when we remove training data from 2014 and up till
April 2015? (We don't know if certain groups were affected much more than
others (i.e. not randomly distributed))

Density bins

- What if errors were not binned by six? What if they were not binned at all?

To figure out scheduling patterns, I decided to use K-Means clustering. Each
schedule has lesson request features (e.g. 2x lesson schedules have
\emph{lr1\_start\_time}, \emph{lr1\_weekday}, \emph{lr2\_start\_time}, and
\emph{lr2\_weekday}). A great visual demonstration of how KMeans algorithm
works can be found online \cite{kmeans:naftali_harris}. First, I looked into
\emph{2x} schedules.  After specifying two clusters as the input, it was able
to split the schedules into morning and evening ones (See Table
\ref{figtab:2_clusters_of_2x_schedules}). However, the members of each cluster
looked like they were all over the place, which suggested that more clusters were
needed. I tried different number of clusters, and 12 seems like a good number
-- the clustering was much tighter (see Table
\ref{figtab:12_clusters_of_2x_schedules}), even for 3x schedules (Table
\ref{figtab:12_clusters_of_3x_schedules}).

What I discovered is that most user schedules, on average, take lessons during
around the same time of day. As one can see, the centroids (in black) of Tables
\ref{figtab:12_clusters_of_2x_schedules} and
\ref{figtab:12_clusters_of_3x_schedules} are mostly horizontal. This validates
the idea that most people are quite habitual with when they take lessons -- such as
mornings, afternoons, evenings, somewhere between morning and afternoons, etc.

\begin{table}[ht]
  \centering
  \begin{tabular}{c@{\quad}cc}
    & a & b \\
    1 & \includegraphics[scale=0.4]{img/cluster_0_out_of_2_clusters_2x.png}\fixedlabel{2-2x-1a}{1a}
    & \includegraphics[scale=0.4]{img/cluster_1_out_of_2_clusters_2x.png}\fixedlabel{2-2x-1b}{1b}
  \end{tabular}
  \caption{2 Clusters of 2x Schedules (n=466)}
  \label{figtab:2_clusters_of_2x_schedules}
\end{table}

\begin{table}[ht]
  \centering
  \begin{tabular}{c@{\quad}ccc}
    & a & b & c\\
    1 & \includegraphics[scale=0.25]{img/cluster_0_out_of_12_clusters_2x.png}\fixedlabel{12-2x-1a}{1a}
    & \includegraphics[scale=0.25]{img/cluster_1_out_of_12_clusters_2x.png}\fixedlabel{12-2x-1b}{1b}
    & \includegraphics[scale=0.25]{img/cluster_2_out_of_12_clusters_2x.png}\fixedlabel{12-2x-2a}{2a} \\ \\
    2 & \includegraphics[scale=0.25]{img/cluster_3_out_of_12_clusters_2x.png}\fixedlabel{12-2x-2b}{2b}
    & \includegraphics[scale=0.25]{img/cluster_4_out_of_12_clusters_2x.png}\fixedlabel{12-2x-3a}{3a}
    & \includegraphics[scale=0.25]{img/cluster_5_out_of_12_clusters_2x.png}\fixedlabel{12-2x-3b}{3b} \\ \\
    3 & \includegraphics[scale=0.25]{img/cluster_6_out_of_12_clusters_2x.png}\fixedlabel{12-2x-4a}{4a}
    & \includegraphics[scale=0.25]{img/cluster_7_out_of_12_clusters_2x.png}\fixedlabel{12-2x-4b}{4b}
    & \includegraphics[scale=0.25]{img/cluster_8_out_of_12_clusters_2x.png}\fixedlabel{12-2x-5a}{5a} \\ \\
    4 & \includegraphics[scale=0.25]{img/cluster_9_out_of_12_clusters_2x.png}\fixedlabel{12-2x-5b}{5b}
     & \includegraphics[scale=0.25]{img/cluster_10_out_of_12_clusters_2x.png}\fixedlabel{12-2x-6a}{6a}
    & \includegraphics[scale=0.25]{img/cluster_11_out_of_12_clusters_2x.png}\fixedlabel{12-2x-6b}{6b}
  \end{tabular}
  \caption{12 Clusters of 2x Schedules (n=466)}
  \label{figtab:12_clusters_of_2x_schedules}
\end{table}

\begin{table}[ht]
  \centering
  \begin{tabular}{c@{\quad}ccc}
    & a & b & c\\
    1 & \includegraphics[scale=0.25]{img/cluster_0_out_of_12_clusters_3x.png}\fixedlabel{block1a}{1a}
    & \includegraphics[scale=0.25]{img/cluster_1_out_of_12_clusters_3x.png}\fixedlabel{block1b}{1b}
    & \includegraphics[scale=0.25]{img/cluster_2_out_of_12_clusters_3x.png}\fixedlabel{block2a}{2a} \\ \\
    2 & \includegraphics[scale=0.25]{img/cluster_3_out_of_12_clusters_3x.png}\fixedlabel{block2b}{2b}
    & \includegraphics[scale=0.25]{img/cluster_4_out_of_12_clusters_3x.png}\fixedlabel{block3a}{3a}
    & \includegraphics[scale=0.25]{img/cluster_5_out_of_12_clusters_3x.png}\fixedlabel{block3b}{3b} \\ \\
    3 & \includegraphics[scale=0.25]{img/cluster_6_out_of_12_clusters_3x.png}\fixedlabel{block4a}{4a}
    & \includegraphics[scale=0.25]{img/cluster_7_out_of_12_clusters_3x.png}\fixedlabel{block4b}{4b}
    & \includegraphics[scale=0.25]{img/cluster_8_out_of_12_clusters_3x.png}\fixedlabel{block5a}{5a} \\ \\
    4 & \includegraphics[scale=0.25]{img/cluster_9_out_of_12_clusters_3x.png}\fixedlabel{block5b}{5b}
     & \includegraphics[scale=0.25]{img/cluster_10_out_of_12_clusters_3x.png}\fixedlabel{block6a}{6a}
    & \includegraphics[scale=0.25]{img/cluster_11_out_of_12_clusters_3x.png}\fixedlabel{block6b}{6b}
  \end{tabular}
  \caption{12 Clusters of 3x Schedules (n=427)}
  \label{figtab:12_clusters_of_3x_schedules}
\end{table}
