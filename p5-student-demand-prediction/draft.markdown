Capstone Project
Machine Learning Engineer Nanodegree
Joe Udacity
December 31st, 2050
Definition

(approximately 1 - 2 pages)
  Project Overview


  In this section, look to provide a high-level overview of the project in layman’s terms. Questions to ask yourself when writing this section:
  Has an overview of the project been provided, such as the problem domain, project origin, and related datasets or input data?
  Has enough background information been given so that an uninformed reader would understand the problem domain and following problem statement?
  Problem Statement

Lingo Live provides customized communication lessons for tech professionals.
We specialize in helping engineers in multinational tech companies (e.g.
Facebook, Google, Twitter); we provide our customers, many of whom are
non-native speakers, a language/communication teacher who knows exactly what
they need, anytime and anywhere. Breaking down language and communication
barriers helps them become more effective communicators, and therefore, better
employees.

It is important for us to make sure that our supply of teachers is able to meet
student demand. As part of the tech team at Lingo Live, one of my
responsibilities is to provide accurate forecasts on our capacity to handle
future students -- do we have enough capacity to handle an influx of new
students? If so, how much more can we handle? If not, how many more teachers do
we need to hire, and what times should they be teaching? Underestimating and
overestimating capacity has serious consequences; not enough teachers means
that some or many students won't be able to get lessons at times that they
want. On the other hand, if we hire too many teachers, many of them might not
get enough lessons, and might have to look at other sources of income to
supplement the income they get from Lingo Live. Thus, getting accurate
forecasts of teacher capacity would help our students and teachers stay happy.

The process of analyzing our capacity involves two main stages. First,
predicting student demand given indirect information (such as timezone of these
students, which company they are working for, a ballpark number of students
that are coming in, and the supposed lesson frequency that people will be
taking).  We would generate a bunch of possible schedules that these new
students might have, based on current student data. Finally, once we have these
predicted schedules, we then compare them with current teacher availability to
see how much we could handle. My focus for this project is only the first stage
-- given timezone and company data, could we generate schedules that are
representative of the new students?

In this project, I compare several strategies and evaluate the effectiveness in
producing representative schedules of potential students: random sampling with
replacement (RSR), a new variation of Synthetic Minority Oversampling Technique
tailored to this problem (SMOTE-SCHED), and Timezone Shifting (TMZ-SHIFT).

Data used in this project is from Lingo Live's production database, anonymized
to protect users' privacy.

  In this section, you will want to clearly define the problem that you are trying to solve, including the strategy (outline of tasks) you will use to achieve the desired solution. You should also thoroughly discuss what the intended solution will be for this problem. Questions to ask yourself when writing this section:
  Is the problem statement clearly defined? Will the reader understand what you are expecting to solve?
  Have you thoroughly discussed how you will attempt to solve the problem?
  Is an anticipated solution clearly defined? Will the reader understand what results you are looking for?

In this project, I explore three strategies to address the problem of
generating schedules that are representative of potential students.  They are
described below.

One strategy is simple random sampling. Given indirect information (timezone,
company, etc.), we could randomly pick (with replacement) a subset of current
students' schedules, and just use those schedules to represent potential
schedules of new students. I hypothesize that this simple way of generating a
set of possible student schedules is probably sufficient, if the subpopulation
we are sampling from has a big enough sample size and is representative of the
population. However, in cases where we are asked to predict student demand from
potential students of an underrepresented timezone, using this simple approach
might be problematic, since it will just create a bunch of clones of members of
the underrepresented timezone, which is probably a statistically biased sample
and not as representative of the population of people belonging in that
timezone.

Another strategy involves creating synthetic data to hopefully address the
issue of random sampling when sample size is small. It is highly inspired by
the Synthetic Minority Oversampling Technique (SMOTE), which was originally
made for classification problems with highly imbalanced datasets *citation*.
The idea is do some sort of interpolation to synthesize new data that would
hopefully be more representative of the population. In generating viable
schedules of underrepresented groups, we randomly pick a schedule, get the
k-nearest neighbors. Then we pick two of those k-nearest neighbors and
interpolate between the two schedules, producing a new schedule that is like
the schedules in the dataset, but not exactly the same. I hypothesize that this
new variation of SMOTE, tailored for this problem (SMOTE-SCHED), will be better
than simple random sampling with replacement when sample size is small.

Finally, the last strategy I explore in this paper is randomly picking a
schedule and adjusting by differences in timezone (TMZ-SHIFT). For example,
let's say we are interested in predicting student demand for people in Eastern
Standard Time. We randomly pick a schedule -- let's pretend it happened to be
that it was from Pacific Standard Time, and that person regularly takes lessons
on Monday, Wednesday, and Friday (MWF) at 6 PM PST. The synthesized schedule
would then have lessons on MWF at 6 PM EST. The underlying assumption is that
most people, with regards to scheduling, are really similar. Most people have a
9-5 job -- they have breakfast, go to work, and go home. They might do lessons
around the same times as well (such as during lunch time, or after work).

To figure out which method is best for simulating data of potential new
students, we do a three-way comparison: RSR vs. SMOTE-SCHED, RSR vs.
TMZ-SHIFT, and SMOTE-SCHED vs. TMZ-SHIFT. Sometimes, we might get 10 new
students, but other times, we might get 300 new ones all at once. Thus, I take
into account number of schedules to be generated as well, see how the
comparisons change as a function of the number of items to be predicted.

For each of the comparisons stated above, we will have a subpopulation group.
The subpopulation is the group of schedules that match the timezone and lesson
frequency of interest.  From that subpopulation, we will divide that into a
test set and a training set.  From the training set, we will generate new data
via the methods described. Then we will use some sort of distance metric to
figure out how far the generated data is from the test set. We will do this
process repeatedly, at least 10,000 times, and we compare the differences
between each of the methods with regards to the test set. Tracking the
differences over many, many iterations would give us confidence intervals that
would support or invalidate some of the hypotheses I described. Doing this
experiment would then inform us on which method is best for predicting student
demand.

