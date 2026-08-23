from fastapi import FastAPI

version = "v1"
app = FastAPI(version=version, title="Modular receipt verefication engine", description="first version will be a verifierapi that will just save and verify bank transactions from certain banks")