# encoding: utf-8
require 'csv'
require 'net/http'
require 'digest/md5'
require 'openssl'
require 'time'


# DIST_DIR="imgs.#{Time.now.to_i}"
DIST_DIR="imgs.chacked"
DIR="$HOME/Dropbox/pokemon-contest/momo_mind/crawler"

#usage: ruby classify.rb download.csv (grade(0-2)) >> (training,test,evaluation).csv


#pokemon_name = ARGV[1]
grade = ARGV[1].to_i
#grade = ARGV[2].to_i
#標準出力

def div(pokemon_name, grade, target)
  counter = 0; # counter
  CSV.foreach(ARGV[0]) do |row|
    keyword = row[0]
    url = row[1]
    dist = row[2]

    begin
      if ((File.exist?("#{DIST_DIR}/#{dist}")) && (keyword == pokemon_name)) then# ファイルが存在
        if ((counter % 3) == grade) then
          #任意のフォルダに移す
          result = `cp #{DIR}/#{DIST_DIR}/#{dist} #{DIR}/#{target}`
          #CSV出力
          puts "#{keyword},#{dist}"
        end
        counter += 1
      end 
    rescue => e
#    puts e.message
    end
  end
end


pokemons = ["ゼニガメ", "ワニノコ", "ミズゴロウ", "ポッチャマ", "ミジュマル", "ケロマツ"]
for pokemon_name in pokemons
#  for grade in 0..2
  case grade
  when 0 then
  #  TAR_DIR = "#{pokemon_name}_training"
    target = "training"
  when 1 then # test
  #  TAR_DIR = "#{pokemon_name}_test"
    target = "test"
  when 2 then # evaluation
  #  TAR_DIR = "#{pokemon_name}_evaluation"
    target = "evaluation"
  else # error
  #  TAR_DIR = "#{pokemon_name}_error"
    target = "error"
  end    
  div(pokemon_name, grade, target)
#  end
end

