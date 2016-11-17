require 'csv'
require 'net/http'
require 'digest/md5'
require 'openssl'
require 'time'

DIST_DIR="imgs.#{Time.now.to_i}"
OUT_CSV_PATH="download_imgs.#{Time.now.to_i}.csv"

unless File.exist?(DIST_DIR)
#  puts "mkdir #{DIST_DIR}"
  Dir.mkdir(DIST_DIR)
end

def fetch(keyword, url)
  uri = URI(url)
#  puts uri
  filename = uri.path.split('/').last
  ext = filename.split('.').last

  req = Net::HTTP::Get.new(uri.request_uri)
  nhttp = Net::HTTP.new(uri.host, uri.port)
  nhttp.use_ssl = uri.scheme == 'https'
  nhttp.verify_mode=OpenSSL::SSL::VERIFY_NONE

  res = nhttp.start() do |http|
    http.request(req)
  end

  md5 = Digest::MD5.hexdigest(res.body)
  dist_path = "#{DIST_DIR}/#{md5}.#{ext}"
  dist = "#{md5}.#{ext}"
#  puts dist_path
  File.open(dist_path, 'w') do |file|
    file.write(res.body)
  end

  dist
end

out_csv = []

CSV.foreach(ARGV[0]) do |row|
  keyword = row[0]
  url = row[1]

  begin
    dist = fetch(keyword, url)
    puts "#{keyword},#{url},#{dist}"
    out_csv << [keyword, url, dist_path, ]
  rescue => e
#    puts e.message
  end
end

#puts "write csv"

File.open(OUT_CSV_PATH, 'a') do |file|
  out_csv.each do |row|
    file.write(row.join(','))
  end
end

