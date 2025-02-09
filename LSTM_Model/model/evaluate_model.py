from sklearn.metrics import accuracy_score

def evaluate_model(model, X_test, y_test):
    """Evaluează modelul pe setul de test"""
    y_pred = (model.predict(X_test) > 0.5).astype(int)
    return accuracy_score(y_test, y_pred)