ARG BASE_CONTAINER=jupyter/minimal-notebook
FROM $BASE_CONTAINER
LABEL author="Deepak Patil"

USER root
RUN pip install pandas numpy matplotlib plotly seaborn urllib

# Switch back to user account to avoid accidental container runs as root
USER $NB_UID