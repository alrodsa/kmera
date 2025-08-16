FROM  python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update -y
RUN apt install -y \
    git \
    python3-pip \
    zsh \
    wget

RUN apt update -y

ARG USERNAME=base-programming
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

RUN pip3 install pdm
# Uses "robbyrussell" theme (original Oh My Zsh theme), with no plugins
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.5/zsh-in-docker.sh)" -- \
    -t robbyrussell

RUN echo "export PATH=$PATH:/home/$USERNAME/.pulumi/bin:/home/$USERNAME/.local/bin" >> ~/.zshrc
