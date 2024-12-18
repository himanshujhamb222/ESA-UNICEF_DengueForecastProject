import os
import glob
from typing import List, Optional
from dataclasses import dataclass
import pandas as pd
import plotly.express as px
from src.commons.logger import logger
from src.commons.constants.paths import PROJECT_FOLDER

@dataclass
class ModelPaths:
    """
    Data class to store paths for different model configurations
    """
    model_name: str
    without_cnn_dir: str
    with_cnn_dir: str


class NRMSEMetricsVisualizer:
    """
    A class to visualize NRMSE metrics for different models
    """

    @staticmethod
    def find_latest_csv(directory: str, model_name: str, with_cnn: bool = False) -> Optional[str]:
        cnn_status = "WITH_CNN" if with_cnn else "WITHOUT_CNN"
        search_pattern = os.path.join(directory, cnn_status, f"{model_name}*.csv")
        matching_files = glob.glob(search_pattern)
        if not matching_files:
            logger.warning(f"No CSV files found for {model_name} {cnn_status}")
            return None
        return max(matching_files, key=os.path.getctime)

    @staticmethod
    def prepare_metric_data(model_files: dict) -> pd.DataFrame:
        try:
            metrics = []
            for model_name, files in model_files.items():
                without_cnn_df = pd.read_csv(files['without_cnn'])
                with_cnn_df = pd.read_csv(files['with_cnn'])

                for df, cnn_status in [(without_cnn_df, 'Without CNN'), (with_cnn_df, 'With CNN')]:
                    for _, row in df.iterrows():
                        metrics.extend([
                            {
                                'Department': row['Department'],
                                'CNN': cnn_status,
                                'Model Name': model_name,
                                'Data': '0-19',
                                'NRMSE': row['NRMSE 0-19 Training'],
                                'Metric Type': 'Training'
                            },
                            {
                                'Department': row['Department'],
                                'CNN': cnn_status,
                                'Model Name': model_name,
                                'Data': '0-19',
                                'NRMSE': row['NRMSE 0-19 Validation'],
                                'Metric Type': 'Validation'
                            },
                            {
                                'Department': row['Department'],
                                'CNN': cnn_status,
                                'Model Name': model_name,
                                'Data': 'All',
                                'NRMSE': row['NRMSE All Training'],
                                'Metric Type': 'Training'
                            },
                            {
                                'Department': row['Department'],
                                'CNN': cnn_status,
                                'Model Name': model_name,
                                'Data': 'All',
                                'NRMSE': row['NRMSE All Validation'],
                                'Metric Type': 'Validation'
                            }
                        ])
            return pd.DataFrame(metrics)
        except Exception as e:
            logger.error(f"Error reading CSV files: {e}")
            raise

    @classmethod
    def plot_nrmse_comparison(cls, model_files: dict, output_dir: str):
        df = cls.prepare_metric_data(model_files)

        # Separate Training and Validation plots
        for metric_type in ['Training', 'Validation']:
            filtered_df = df[df['Metric Type'] == metric_type]
            fig = px.bar(
                filtered_df,
                x='Department',
                y='NRMSE',
                color='CNN',
                facet_col='Model Name',  # Facet by Model Name
                facet_row='Data',        # Facet by Data ('0-19' and 'All')
                title=f"{metric_type} NRMSE Comparison",
                barmode='group',         # Group bars for With CNN and Without CNN
                height=700, width=1500
            )
            fig.update_layout(
                xaxis_title='Department',
                yaxis_title='NRMSE',
                font=dict(size=12)
            )
            fig.show()

            # Save plot
            output_file = os.path.join(output_dir, f"{metric_type.lower()}_nrmse_comparison.html")
            os.makedirs(output_dir, exist_ok=True)
            fig.write_html(output_file)
            logger.info(f"Saved plot: {output_file}")

def get_model_paths(base_directory: str) -> List[ModelPaths]:
    return [
        ModelPaths('catboost', os.path.join(base_directory, "code/metrics/Brazil"),
                   os.path.join(base_directory, "code/metrics/Brazil")),
        ModelPaths('lstm', os.path.join(base_directory, "code/metrics/Brazil"),
                   os.path.join(base_directory, "code/metrics/Brazil")),
        ModelPaths('svm', os.path.join(base_directory, "code/metrics/Brazil"),
                   os.path.join(base_directory, "code/metrics/Brazil")),
        ModelPaths('rf', os.path.join(base_directory, "code/metrics/Brazil"),
                   os.path.join(base_directory, "code/metrics/Brazil"))
    ]

def generate_nrmse_plots(model_paths: List[ModelPaths], output_directory: str):
    visualizer = NRMSEMetricsVisualizer()
    model_files = {}

    for model_config in model_paths:
        without_cnn = visualizer.find_latest_csv(model_config.without_cnn_dir, model_config.model_name, with_cnn=False)
        with_cnn = visualizer.find_latest_csv(model_config.with_cnn_dir, model_config.model_name, with_cnn=True)
        if not (without_cnn and with_cnn):
            logger.warning(f"Skipping {model_config.model_name} due to missing files")
            continue
        model_files[model_config.model_name] = {'without_cnn': without_cnn, 'with_cnn': with_cnn}

    visualizer.plot_nrmse_comparison(model_files, output_directory)

def main():
    try:
        output_dir = os.path.join(PROJECT_FOLDER, 'code/metrics/visualization')
        model_paths = get_model_paths(base_directory=PROJECT_FOLDER)
        generate_nrmse_plots(model_paths, output_dir)
        logger.info("NRMSE metrics visualization completed successfully.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
