import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np

def create_weather_risk_model(input_shape=(5,)):
    """
    Create a deep learning model for weather risk assessment
    
    Args:
        input_shape: Shape of input features (temperature, humidity, wind_speed, precipitation, pressure)
    
    Returns:
        Compiled tensorflow model
    """
    model = models.Sequential([
        layers.Dense(64, activation='relu', input_shape=input_shape),
        layers.Dropout(0.2),
        layers.Dense(32, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(16, activation='relu'),
        layers.Dense(1, activation='sigmoid')
    ])
    
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def train_model(X_train, y_train, X_val, y_val, epochs=50, batch_size=32):
    """
    Train the weather risk assessment model
    
    Args:
        X_train: Training features
        y_train: Training labels
        X_val: Validation features
        y_val: Validation labels
        epochs: Number of training epochs
        batch_size: Batch size for training
    
    Returns:
        Trained model and training history
    """
    model = create_weather_risk_model(input_shape=X_train.shape[1:])
    
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=epochs,
        batch_size=batch_size,
        callbacks=[
            tf.keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=5,
                restore_best_weights=True
            )
        ]
    )
    
    return model, history

def evaluate_model(model, X_test, y_test):
    """
    Evaluate model performance on test data
    
    Args:
        model: Trained model
        X_test: Test features
        y_test: Test labels
    
    Returns:
        Dictionary containing evaluation metrics
    """
    loss, accuracy = model.evaluate(X_test, y_test)
    predictions = model.predict(X_test)
    
    # Calculate additional metrics
    predictions_binary = (predictions > 0.5).astype(int)
    
    true_positives = np.sum((predictions_binary == 1) & (y_test == 1))
    false_positives = np.sum((predictions_binary == 1) & (y_test == 0))
    false_negatives = np.sum((predictions_binary == 0) & (y_test == 1))
    
    precision = true_positives / (true_positives + false_positives)
    recall = true_positives / (true_positives + false_negatives)
    f1_score = 2 * (precision * recall) / (precision + recall)
    
    return {
        'loss': loss,
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1_score
    }
