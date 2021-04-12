FROM ubuntu:18.04
RUN apt update && apt install -y  python3-pip git golang-go make bison
RUN git clone https://hub.fastgit.org/xuperchain/contract-sdk-py.git
RUN cd contract-sdk-py && pip3 install -r requirements.txt -i https://pypi.douban.com/simple

RUN  apt install -y wget curl
RUN wget https://raw.staticdn.net/moovweb/gvm/master/binscripts/gvm-installer
RUN git config --global url."https://hub.fastgit.org".insteadOf https://github.com
RUN bash gvm-installer
#RUN bash < <(curl -s -S -L https://raw.githubusercontent.com/moovweb/gvm/master/binscripts/gvm-installer)
#RUN bash -c "bash < <(curl -s -S -L https:// raw.staticdn.net/moovweb/gvm/master/binscripts/gvm-installer)"

RUN bash -c "source /root/.gvm/scripts/gvm && gvm install go1.13 && gvm use go1.13"
RUN git clone https://hub.fastgit.org/xuperchain/xuperchain.git
RUN bash -c "cd xuperchain && source /root/.gvm/scripts/gvm && gvm use go1.13 &&  GOPROXY=goproxy.cn make"
RUN cd /contract-sdk-py && python3 setup.py install
RUN apt install -y vim

WORKDIR /xuperchain/output
#RUN sed -i  's/enable: false/enable: true/g' conf/xchain.yaml
COPY xchain.yaml /xuperchain/output/conf/xchain.yaml
RUN ./xchain-cli createChain

CMD ./xchain
#RUN ./xchain-cli account new --account 1111111111111111 --fee 2000000000000 && ./xchain-cli transfer --to XC1111111111111111@xuper --amount 10000000000000000
#RUN ./xchain-cli native deploy --account XC1111111111111111@xuper  -a '{"creator":"xchain"}' --fee 15587517 --runtime py  --cname counter ../../contract-sdk-py/example/counter/counter.py

#RUN ./xchain-cli native invoke --method Increase -a '{"key":"xchain"}' features --fee 1