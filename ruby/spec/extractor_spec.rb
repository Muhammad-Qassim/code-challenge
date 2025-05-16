require 'rspec'
require 'json'
require_relative '../extractor'

RSpec.describe 'extracting_data_from_html' do
  let(:input_path) { File.expand_path('../../../files/van-gogh-paintings.html', __FILE__) }
  let(:output_path) { File.expand_path('../../../files/expected-array.json', __FILE__) }

  before(:each) do
    File.delete(output_path) if File.exist?(output_path)
  end

  it 'extracts structured data from a HTML file and writes to JSON' do
    html = File.read(input_path)
    result = extracting_data_from_html(html, output_path)

    expect(File).to exist(output_path)
    expect(result).to be_a(Hash)
    expect(result.keys.first).to be_a(String)

    items = result.values.first
    expect(items).to be_an(Array)
    expect(items.first).to include(:name, :extensions, :link, :image)
  end

  after(:each) do
    File.delete(output_path) if File.exist?(output_path)
  end
end
