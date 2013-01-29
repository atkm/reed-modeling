% \iffalse meta-comment
% 
%   reedmcm.cls -- A LaTeX class to produce reports for the MCM contest.
%                   
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{reedmcm}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax %% <-- fix if we decide to declare some options!
\LoadClass[11pt]{article}

%% Get some useful information about errors.
\setcounter{errorcontextlines}{25}

\RequirePackage{lastpage} % to use \pageref{LastPage}
\RequirePackage{xspace} % use \xspace in command definitions
\RequirePackage{verbatim}
\RequirePackage{booktabs} % toprule, middlerule, bottomrule

%%% Define a command to take the letter of the question answered.
\newcommand{\@question}[1]{}
\newcommand{\question}[1]{\gdef\@question{#1}}
\global\let\@question\relax

%%% Define a command to take the contest.
\newcommand{\@contest}[1]{}
\newcommand{\contest}[1]{\gdef\@contest{#1}}
\global\let\@contest\relax


%%% Define a command for the ``team control number'', which is the
%%% only allowable identifier on the paper.
%%% We also redefine \@author here, to ensure that the only author
%%% information included in the document is the team number specified
%%% by the contest runners.
\newcommand{\@team}[1]{}
\newcommand{\team}[1]{\gdef\@team{#1}}


%%% Redefine the \maketitle command to include our extra information.

\def\@maketitle{%
  \newpage
  \null
  \vskip 2em%
  \begin{center}%
  \let \footnote \thanks
    {\LARGE \@title \par}%
    \vskip 1em%
    {\Large \@contest\ Contest Question \@question}
    \vskip 1.5em%
    {\large
      \lineskip .5em%
      \begin{tabular}[t]{c}%
        Team \# \@team
      \end{tabular}\par}%
    \vskip 1em%
    {\large \@date}%
  \end{center}%
  \par
  \vskip 1.5em}


%%% Define a ``summary'' environment that will appear on a separate
%%% page.

\newenvironment{summary}{%
  \vspace{2.5in}
      \null\vfil
      \@beginparpenalty\@lowpenalty
  \thispagestyle{empty}
      \begin{center}%
        \bfseries Summary
        \@endparpenalty\@M
      \end{center}
}{\newpage%
\setcounter{page}{1}}%


\AtEndDocument{%
\typeout{}
\typeout{Remember, do not put the names of any team members,}
\typeout{your advisor, or your institution in the document!}
\typeout{}
}
