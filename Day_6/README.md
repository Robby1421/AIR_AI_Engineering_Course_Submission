### 1. **Data Quality Monitoring Agent**

**Role**: 
The Data Quality Monitoring Agent ensures the integrity, consistency, and cleanliness of the dataset. It performs several key functions to maintain the accuracy of the data and prepares it for further analysis.

**What It Does**:
- **Data Cleaning**: The agent removes unwanted characters (such as '₱' symbol and commas) from the dataset, particularly in columns like `ad spend` and `revenue`, and converts the columns to a numeric format.
- **Missing Values Check**: It checks for any missing or `NaN` values in the dataset, which might affect the analysis.
- **Duplicates Check**: The agent identifies duplicate rows in the dataset that could distort analysis results.
- **Data Type Validation**: It ensures that each column contains the correct data type (e.g., numeric data in the `ad spend` column).
- **Summary**: After performing these checks, it generates a summary report, providing an overview of the dataset's quality and any issues that need attention.

**Outcome**: 
- A cleaned dataset with proper data types.
- A report on missing values, duplicates, and any other data quality issues.


### 2. **Data Lineage Tracking Agent**

**Role**: 
The Data Lineage Tracking Agent traces the flow and transformation of data through various stages, from its source to its final destination. This is important for understanding how data is processed, transformed, and consumed in different systems. It ensures transparency, compliance, and effective debugging in data pipelines.

**What It Does**:
- **Track Data Source**: The agent records the source of the data (e.g., marketing campaign, internal system, third-party service) and logs the initial state of the dataset.
- **Track Transformations**: It tracks any transformations applied to the data (e.g., currency conversions, data cleaning) and logs details about what was changed, including the operation and the effect on the data.
- **Track Data Destination**: The agent logs where the data is sent after transformations (e.g., to a reporting database, data warehouse, or analytics platform).
- **Generate Lineage Report**: After all transformations are tracked, the agent generates a detailed report summarizing the entire data lineage, including the flow from source to destination and any transformations applied along the way.
- **Visualize Lineage**: It provides a textual summary or visualization of the data lineage, offering stakeholders an understanding of how the data has evolved and moved across systems.

**Outcome**: 
- A detailed log of data's journey, including source, transformations, and destinations.
- A report or visualization summarizing the data lineage, helping teams track and understand the data flow.

---

### 3. **Data Security Compliance Agent**

**Role**: 
The Data Security Compliance Agent ensures that data is managed in a secure and compliant manner, following data protection laws, regulations, and internal security protocols. This agent helps to monitor and safeguard sensitive data to mitigate risks related to data breaches or non-compliance.

**What It Does**:
- **Monitor Sensitive Data**: The agent checks for the presence of sensitive information (e.g., personally identifiable information, financial data) in the dataset. It identifies columns containing sensitive data that may require encryption or redaction.
- **Data Access Control**: It ensures that proper access controls are in place, restricting unauthorized access to sensitive data. The agent checks if access permissions are aligned with security policies.
- **Compliance Check**: It validates the dataset against relevant data protection laws and regulations, such as GDPR, HIPAA, or other industry-specific standards. This includes checking if data handling practices (e.g., data collection, storage, processing, and sharing) comply with legal requirements.
- **Audit and Logging**: The agent tracks and logs any access or changes to sensitive data, creating an audit trail that can be used for security analysis and compliance reporting.
- **Encrypt Sensitive Data**: If required, the agent can apply encryption or redaction techniques to sensitive data to prevent unauthorized exposure.

**Outcome**:
- A dataset that is secure and compliant with legal requirements.
- An audit trail of data access and changes for future analysis and compliance checks.
- Recommendations for improving data security practices, such as better access control or data encryption.

---

### Summary of Agent Roles:
- **Data Quality Monitoring Agent**: Ensures the dataset is clean, consistent, and accurate by handling missing values, duplicates, and incorrect data types.
- **Data Lineage Tracking Agent**: Tracks the flow and transformations of data, providing transparency and accountability in data handling.
- **Data Security Compliance Agent**: Ensures that sensitive data is protected, and that the dataset complies with relevant data security laws and regulations.

Each of these agents plays a critical role in maintaining the integrity, security, and traceability of data within a larger data pipeline or system. Together, they support the broader goals of data governance, making sure that data is accurate, secure, and used responsibly.
