require 'rspec'
require 'json'
require 'fileutils'
require_relative File.expand_path('../extractor', __dir__)

RSpec.describe 'extracting_data_from_html' do
  let(:base_dir) { File.expand_path('../../files', __dir__) }
  let(:output_path) { File.join(base_dir, 'test-output.json') }

  def run_extraction_test(filename)
    input_path = File.join(base_dir, filename)
    FileUtils.rm_f(output_path)

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
    FileUtils.rm_f(output_path)
  end

  it 'extracts from van-gogh-paintings.html' do
    run_extraction_test('van-gogh-paintings.html')
  end

  it 'extracts from leo-da-vinci-paintings.html' do
    run_extraction_test('leo-da-vinci-paintings.html')
  end

  it 'extracts from raphael-paintings.html' do
    run_extraction_test('raphael-paintings.html')
  end
end
