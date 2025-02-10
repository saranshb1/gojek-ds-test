
.PHONY: setup_env remove_env data features train predict run clean test
PROJECT_NAME=work-at-gojek


ifeq ($(OS),Windows_NT)
    HAS_PYENV=False
    CONDA_ROOT=$(shell conda info --base)
#   BINARIES = ${CONDA_ROOT}\envs\${PROJECT_NAME}\Scripts
	BINARIES = ${CONDA_ROOT}\envs\${PROJECT_NAME}
else
    ifeq (,$(shell which pyenv))
        HAS_PYENV=False
        CONDA_ROOT=$(shell conda info --root)
        BINARIES = ${CONDA_ROOT}/envs/${PROJECT_NAME}/bin
    else
        HAS_PYENV=True
        CONDA_VERSION=$(shell echo $(shell pyenv version | awk '{print $$1;}') | awk -F "/" '{print $$1}')
        BINARIES = $(HOME)/.pyenv/versions/${CONDA_VERSION}/envs/${PROJECT_NAME}/bin
    endif
endif

setup_env:
ifeq ($(OS),Windows_NT)
	@echo ">>> Creating conda environment."
#	conda env create --name $(PROJECT_NAME) -f environment.yaml --force
	conda env create --name $(PROJECT_NAME) -f environment.yaml -v
	@echo ">>> Activating new conda environment"
	@call activate $(PROJECT_NAME)
else
	@echo ">>> Creating conda environment."
	conda env create --name $(PROJECT_NAME) -f environment.yaml --force
	@echo ">>> Activating new conda environment"
	source $(CONDA_ROOT)/bin/activate $(PROJECT_NAME)
endif

remove_env:
	@echo ">>> Removing conda environment"
	conda remove -n $(PROJECT_NAME) --all

activate:
	conda init $(PROJECT_NAME)
	conda activate $(PROJECT_NAME)


#For windows, force command prompt usage
SHELL := cmd.exe

data:
	@echo "Creating dataset from booking_log and participant_log.."
	${BINARIES}/python.exe -m src.data.make_dataset

features:
	@echo "Running feature engineering on dataset.."
	${BINARIES}/python.exe -m src.features.build_features

train:
	@echo "Training classification model for allocation task.."
	${BINARIES}/python.exe -m src.models.train_model

predict:
	@echo "Performing model inference to identify best drivers.."
	${BINARIES}/python.exe -m src.models.predict_model

test:
	@echo "Running all unit tests.."
	${BINARIES}/nosetests --nologcapture

run: 
#	@$(MAKE) remove_env
#	@$(MAKE) setup_env
#	@$(MAKE) activate
#	@$(MAKE) clean
	@$(MAKE) data
	@$(MAKE) features
	@$(MAKE) train
	@$(MAKE) predict
	@$(MAKE) test

clean:
	@find . -name "*.pyc" -exec rm {} \;
	@rm -f data/processed/* models/* submission/*;

echo_binaries:
	@echo ${BINARIES}
