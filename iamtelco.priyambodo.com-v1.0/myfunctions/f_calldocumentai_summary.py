from typing import Optional
import os
import re
from google.api_core.client_options import ClientOptions
from google.cloud import documentai_v1beta3 as documentai

vPROJECT_ID = os.environ.get('GCP_PROJECT')          #Your Google Cloud Project ID
vLOCATION = os.environ.get('GCP_REGION')             #Your Google Cloud Project Region

# TODO(developer): Uncomment these variables before running the sample.
project_id = vPROJECT_ID
location = "us" # Format is "us" or "eu"
processor_id = "dd5b50441d53f49d" # Create processor before running sample
processor_version = "fddf2b010581ffe1" # Refer to https://cloud.google.com/document-ai/docs/manage-processor-versions for more information
file_path = "/path/to/local/pdf"
mime_type = "application/pdf" # Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types
processor_url = "https://us-documentai.googleapis.com/v1/projects/388889235558/locations/us/processors/dd5b50441d53f49d/processorVersions/fddf2b010581ffe1:process"

def f_process_document_summarizer(
    project_id: str,
    location: str,
    processor_id: str,
    processor_version: str,
    file_path: str,
    mime_type: str,
    vLength: str = "COMPREHENSIVE",
    vFormat: str = "PARAGRAPH",
):
    print(file_path)
    # For supported options, refer to:
    # https://cloud.google.com/document-ai/docs/reference/rest/v1beta3/projects.locations.processors.processorVersions#summaryoptions
    if vLength == "Auto":
        vLength = documentai.SummaryOptions.Length.LENGTH_UNSPECIFIED
    if vLength == "Brief":
        vLength = documentai.SummaryOptions.Length.BRIEF
    if vLength == "Moderate":
        vLength = documentai.SummaryOptions.Length.MODERATE
    if vLength == "Comprehensive":
        vLength = documentai.SummaryOptions.Length.COMPREHENSIVE

    if vFormat == "Auto":
        vFormat = documentai.SummaryOptions.Format.FORMAT_UNSPECIFIED
    if vFormat == "Paragraph":
        vFormat = documentai.SummaryOptions.Format.PARAGRAPH
    if vFormat == "Bullets":
        vFormat = documentai.SummaryOptions.Format.BULLETS

    summary_options = documentai.SummaryOptions(
        length=vLength,
        format=vFormat,
    )

    properties = [
        documentai.DocumentSchema.EntityType.Property(
            name="summary",
            value_type="string",
            #occurence_type=documentai.DocumentSchema.EntityType.Property.OccurenceType.REQUIRED_ONCE,
            property_metadata=documentai.PropertyMetadata(
                field_extraction_metadata=documentai.FieldExtractionMetadata(
                    summary_options=summary_options
                )
            ),
        )
    ]

    # Optional: Request specific summarization format other than the default
    # for the processor version.
    process_options = documentai.ProcessOptions(
        schema_override=documentai.DocumentSchema(
            entity_types=[
                documentai.DocumentSchema.EntityType(
                    name="summary_document_type",
                    base_types=["document"],
                    properties=properties,
                )
            ]
        )
    )

    # Online processing request to Document AI
    document = process_document(
        project_id,
        location,
        processor_id,
        processor_version,
        file_path,
        mime_type,
        process_options=process_options,
    )

    for entity in document.entities:
        returned_value = print_entity(entity)
        # Print Nested Entities (if any)
        for prop in entity.properties:
            returned_value = print_entity(prop)
        return returned_value 


def print_entity(entity: documentai.Document.Entity):
    # Fields detected. For a full list of fields for each processor see
    # the processor documentation:
    # https://cloud.google.com/document-ai/docs/processors-list
    key = entity.type_

    # Some other value formats in addition to text are availible
    # e.g. dates: `entity.normalized_value.date_value.year`
    text_value = entity.text_anchor.content
    confidence = entity.confidence
    normalized_value = entity.normalized_value.text
    print("-----------------------------------------------------------------------")
    print(f"    * {repr(key)}: {repr(text_value)}({confidence:.1%} confident)")
    print("-----------------------------------------------------------------------")
    if normalized_value:
        print(f"    * Normalized Value: {repr(normalized_value)}")
        print("-----------------------------------------------------------------------")
        cleaned_text = normalized_value
        #cleaned_text = re.sub(r"'", "", cleaned_text)
        print(cleaned_text)
        return cleaned_text
    else:
        return "The Result is Not Available, Please Try Other Document"  # Return an empty string if normalized_value is not available

def process_document(
    project_id: str,
    location: str,
    processor_id: str,
    processor_version: str,
    file_path: str,
    mime_type: str,
    process_options: Optional[documentai.ProcessOptions] = None,
) -> documentai.Document:
    # You must set the `api_endpoint` if you use a location other than "us".
    client = documentai.DocumentProcessorServiceClient(
        client_options=ClientOptions(
            api_endpoint=f"{location}-documentai.googleapis.com"
        )
    )

    # The full resource name of the processor version, e.g.:
    # `projects/{project_id}/locations/{location}/processors/{processor_id}/processorVersions/{processor_version_id}`
    # You must create a processor before running this sample.
    name = client.processor_version_path(
        project_id, location, processor_id, processor_version
    )

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Configure the process request
    request = documentai.ProcessRequest(
        name=name,
        raw_document=documentai.RawDocument(content=image_content, mime_type=mime_type),
        # Only supported for Document OCR processor
        process_options=process_options,
    )

    result = client.process_document(request=request)

    # For a full list of `Document` object attributes, reference this page:
    # https://cloud.google.com/document-ai/docs/reference/rest/v1/Document
    return result.document

# [END documentai_process_document_summarizer]