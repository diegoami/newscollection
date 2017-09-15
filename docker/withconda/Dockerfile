FROM ubuntu:16.04

MAINTAINER Diego Amicabile <diego.amicabile@gmail.com>

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN apt-get update --fix-missing && apt-get install -y wget bzip2 ca-certificates \
    libglib2.0-0 libxext6 libsm6 libxrender1 \
    git mercurial subversion

RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh && \
    wget --quiet https://repo.continuum.io/archive/Anaconda3-4.4.0-Linux-x86_64.sh -O ~/anaconda.sh && \
    /bin/bash ~/anaconda.sh -b -p /opt/conda && \
    rm ~/anaconda.sh

RUN apt-get install -y curl grep sed dpkg && \
    TINI_VERSION=`curl https://github.com/krallin/tini/releases/latest | grep -o "/v.*\"" | sed 's:^..\(.*\).$:\1:'` && \
    curl -L "https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini_${TINI_VERSION}.deb" > tini.deb && \
    dpkg -i tini.deb && \
    rm tini.deb && \
    apt-get clean

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

ENV PATH /opt/conda/bin:$PATH

RUN cd ~ && mkdir .ssh && cp /app/.ssh/* ~/.ssh

RUN conda install -y requests lxml pyyaml cssselect

RUN cd ~ && git clone https://github.com/diegoami/newscollection.git

RUN cd ~/newscollection/scrapers && git clone git@github.com:diegoami/techcrunch-posts-scraper.git

RUN cd ~/newscollection/scrapers/techcrunch-posts-scraper && python scrape.py

RUN git add * && git commit -a -m "Latest news" && git push origin master



ENTRYPOINT [ "/usr/bin/tini", "--" ]
CMD [ "/bin/bash" ]

