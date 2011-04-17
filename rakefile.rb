task :default do
    sh "coffee -c -b bubble.coffee"
end

task :tasks do
    sh "python generate_tasks.py"
end

task :build => [:tasks,:default]

task :install_node_js do
    sh "sudo apt-get install python-software-properties"
    sh "sudo add-apt-repository ppa:jerome-etienne/neoip"
    sh "sudo apt-get update"
    sh "sudo apt-get install nodejs"    
end

task :install_npm do
    sh "curl http://npmjs.org/install.sh | sudo sh"
end

task :install_coffeescript do
    sh "npm install coffee-script"
end

task :install => [:install_node_js, 
                :install_npm, 
                :install_coffeescript]
